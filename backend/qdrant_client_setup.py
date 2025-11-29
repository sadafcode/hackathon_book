import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
from backend.qdrant_config import QDRANT_HOST, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, QDRANT_VECTOR_SIZE

load_dotenv()

def initialize_qdrant_client():
    client = QdrantClient(
        host=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
    )
    return client

def create_qdrant_collection(client: QdrantClient):
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=QDRANT_VECTOR_SIZE, distance=models.Distance.COSINE),
    )
    print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully.")

if __name__ == "__main__":
    # Example usage: Ensure you have QDRANT_HOST and QDRANT_API_KEY set in your .env file
    client = initialize_qdrant_client()
    create_qdrant_collection(client)
