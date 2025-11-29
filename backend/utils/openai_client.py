import os
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer # New import

load_dotenv()

# Configure Google Generative AI for chat completion with API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)

# Hugging Face Embedding Model
HF_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # Recommended free model
hf_embedding_model = SentenceTransformer(HF_EMBEDDING_MODEL_NAME) # Initialize the HF model

# Google's generative model identifier
GENERATIVE_MODEL = "models/gemini-pro-latest" # More stable and widely available Gemini model

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using a Hugging Face SentenceTransformer model."""
    embedding = hf_embedding_model.encode(text).tolist()
    return embedding

def get_chat_completion(messages: list[dict], temperature: float = 0.7) -> str:
    """Gets a chat completion from Google's generative model."""
    model = genai.GenerativeModel(GENERATIVE_MODEL)

    system_prompt = ""
    user_query_with_context = ""

    if messages and messages[0]["role"] == "system":
        system_prompt = messages[0]["content"]
        if len(messages) > 1 and messages[-1]["role"] == "user":
            user_query_with_context = messages[-1]["content"]
    elif messages and messages[0]["role"] == "user":
        user_query_with_context = messages[0]["content"]

    full_gemini_prompt = f"{system_prompt}\n\n{user_query_with_context}".strip()
    
    if not full_gemini_prompt:
        return "Error: No content provided for Gemini prompt."

    response = model.generate_content(
        contents=[{"role": "user", "parts": [full_gemini_prompt]}],
        generation_config=genai.types.GenerationConfig(temperature=temperature)
    )
    
    return response.text
