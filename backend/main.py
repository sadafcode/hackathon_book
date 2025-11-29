from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from utils.openai_client import get_embedding, get_chat_completion, GENERATIVE_MODEL
from utils.qdrant_client import search_vectors, create_collection_if_not_exists, COLLECTION_NAME
from utils.postgres_client import init_db, get_chunks_by_ids

app = FastAPI()

# Configure CORS to allow communication from your Docusaurus frontend
origins = [
    "http://localhost:3000",  # Allow Docusaurus dev server
    "http://localhost:8000",  # Allow FastAPI dev server itself
    # Add your deployed Docusaurus URL here in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    source_urls: list[str] = []

# --- Startup Events ---
@app.on_event("startup")
async def startup_event():
    print("Initializing database and Qdrant collection...")
    await init_db()
    create_collection_if_not_exists()
    print("Database and Qdrant collection initialized.")

# --- Endpoints ---
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        if request.selected_text:
            # If selected_text is provided, use it as the primary context
            messages = [
                {"role": "system", "content": "You are a helpful assistant. Answer the user's question based *only* on the provided SELECTED TEXT. If the answer is not in the SELECTED TEXT, clearly state that you do not have enough information from the selection."},
                {"role": "user", "content": f"SELECTED TEXT:\n---\n{request.selected_text}\n---\n\nQuestion: {request.query}\n\nAnswer:"}
            ]
            response_content = get_chat_completion(messages, temperature=0.2)
            return ChatResponse(response=response_content, source_urls=[])
        else:
            # Standard RAG: Generate embedding for query, search Qdrant, retrieve from Postgres
            query_embedding = get_embedding(request.query)
            hits = search_vectors(query_embedding)

            if not hits:
                return ChatResponse(response="I couldn't find any relevant information in the book to answer your question.", source_urls=[])

            chunk_ids = [hit.payload["chunk_id"] for hit in hits if "chunk_id" in hit.payload]
            if not chunk_ids:
                return ChatResponse(response="I found some relevant vectors, but couldn't link them to specific content. Please try re-ingesting your data if this persists.", source_urls=[])

            # Retrieve full content and metadata from Postgres
            chunks_metadata = await get_chunks_by_ids(chunk_ids)

            if not chunks_metadata:
                return ChatResponse(response="I retrieved relevant IDs, but no content was found in the database. The ingestion might be incomplete or incorrect.", source_urls=[])

            # Assemble context for the LLM
            retrieved_context = "\n\n---\n\n".join([chunk.content for chunk in chunks_metadata])
            source_urls = list(set([chunk.source_url for chunk in chunks_metadata]))

            messages = [
                {"role": "system", "content": "You are a helpful assistant for a textbook on Physical AI & Humanoid Robotics. Answer the user's question concisely based *only* on the following context from the book. If the answer is not explicitly in the context, state that you don't know. Do not invent information. If you cite sources, refer to them generally as 'the book' or 'the relevant section'."},
                {"role": "user", "content": f"Context:\n---\n{retrieved_context}\n---\n\nQuestion: {request.query}\n\nAnswer:"}
            ]
            response_content = get_chat_completion(messages, temperature=0.2)
            return ChatResponse(response=response_content, source_urls=source_urls)

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
