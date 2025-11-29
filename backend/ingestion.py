import os
import glob
import re
import uuid
from dotenv import load_dotenv
from utils.openai_client import get_embedding
from utils.qdrant_client import create_collection_if_not_exists, upsert_vectors, COLLECTION_NAME
from utils.postgres_client import init_db, bulk_insert_chunk_metadata, ChunkMetadata
from qdrant_client import models

load_dotenv()

# --- Text Processing Utilities ---

def clean_markdown_content(markdown_content: str) -> str:
    """Strips Docusaurus frontmatter, JSX, and code blocks to get clean text."""
    # Remove Docusaurus frontmatter (YAML block at the top)
    cleaned_content = re.sub(r'^---\n[\s\S]*?\n---\n', '', markdown_content, flags=re.MULTILINE)
    # Remove JSX components (e.g., <Tabs>, <TabItem>, <Link>)
    cleaned_content = re.sub(r'<[A-Z][^>]*>.*?<\/[A-Z][^>]*>|<[A-Z][^>]*\/>', '', cleaned_content, flags=re.DOTALL)
    # Remove code blocks (fenced code blocks ```...```)
    cleaned_content = re.sub(r'```[\s\S]*?```', '', cleaned_content)
    # Remove inline code `...`
    cleaned_content = re.sub(r'`[^`]*`', '', cleaned_content)
    # Remove Markdown links and images [text](url)
    cleaned_content = re.sub(r'!\[.*\]\(.*\)', '', cleaned_content)
    cleaned_content = re.sub(r'\[.*\]\(.*\)', '', cleaned_content)
    # Remove HTML tags that might remain (e.g., <br/>)
    cleaned_content = re.sub(r'<[^>]*>', '', cleaned_content)
    # Replace multiple newlines/spaces with a single space or newline
    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content).strip()
    return cleaned_content

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Splits text into chunks with a specified size and overlap."""
    # A simple, character-based chunking strategy
    # In a real application, consider token-based chunking or more advanced splitters
    chunks = []
    if not text: return chunks

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text): # Reached end of text
            break
        start += chunk_size - chunk_overlap
        # Ensure start doesn't go negative if chunk_size < chunk_overlap (though invalid params)
        start = max(0, start)
    return chunks

# --- Ingestion Process ---

async def ingest_documents(base_path: str = ".."): # Default to parent directory (project root) assuming script is run from backend/
    await init_db() # Ensure Postgres table is created
    create_collection_if_not_exists() # Ensure Qdrant collection is created

    markdown_files = glob.glob(os.path.join(base_path, "docs", "**", "*.md"), recursive=True) + \
                     glob.glob(os.path.join(base_path, "docs", "**", "*.mdx"), recursive=True) + \
                     glob.glob(os.path.join(base_path, "blog", "**", "*.md"), recursive=True) + \
                     glob.glob(os.path.join(base_path, "blog", "**", "*.mdx"), recursive=True)

    all_qdrant_points = []
    all_postgres_chunks_data = []

    print(f"Found {len(markdown_files)} markdown files to ingest.")

    for file_path in markdown_files:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = clean_markdown_content(content)
        if not cleaned_content.strip():
            print(f"Skipping empty or cleaned-out file: {file_path}")
            continue

        chunks = chunk_text(cleaned_content)

        for i, chunk_content in enumerate(chunks):
            if not chunk_content.strip():
                continue

            chunk_id = str(uuid.uuid4())
            embedding = get_embedding(chunk_content)

            # Prepare for Qdrant
            all_qdrant_points.append(models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={"chunk_id": chunk_id} # Store chunk_id in payload for retrieval linkage
            ))

            # Prepare for Postgres
            # Deduce source_url from file_path relative to base_path and Docusaurus structure
            relative_path = os.path.relpath(file_path, base_path).replace('\\', '/') # Use forward slashes
            # Docusaurus docs are usually at /, blogs at /blog/
            source_url = relative_path.replace("docs/", "/").replace("blog/", "/blog/").replace(".mdx", "").replace(".md", "")
            # Adjust for index files if needed, e.g., /index -> /
            if source_url.endswith("/index"):
                source_url = source_url[:-len("index")]
            if source_url.endswith("/") and len(source_url) > 1:
                source_url = source_url[:-1] # Remove trailing slash unless it's root

            all_postgres_chunks_data.append({
                "id": chunk_id,
                "content": chunk_content,
                "source_url": source_url,
                "page_number": i + 1, # Simple page number approximation
                "start_char": content.find(chunk_content), # This is a rough approx
                "end_char": content.find(chunk_content) + len(chunk_content),
            })

    if all_qdrant_points:
        print(f"Upserting {len(all_qdrant_points)} vectors to Qdrant...")
        upsert_vectors(all_qdrant_points)
        print("Qdrant upsertion complete.")

    if all_postgres_chunks_data:
        print(f"Bulk inserting {len(all_postgres_chunks_data)} chunk metadata to Postgres...")
        await bulk_insert_chunk_metadata(all_postgres_chunks_data)
        print("Postgres bulk insertion complete.")

    print("Ingestion process finished.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(ingest_documents())
