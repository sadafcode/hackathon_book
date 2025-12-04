import os

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "book_content"

# This should match the dimension of your embedding model
# Using sentence-transformers/all-MiniLM-L6-v2 which outputs 384 dimensions
QDRANT_VECTOR_SIZE = 384
