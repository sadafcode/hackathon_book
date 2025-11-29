import os

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "book_content"

# This should match the dimension of your embedding model (e.g., 1536 for OpenAI's text-embedding-ada-002)
QDRANT_VECTOR_SIZE = 1536
