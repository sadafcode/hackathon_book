import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "chatbot_knowledge")
VECTOR_SIZE = 384 # Matches sentence-transformers/all-MiniLM-L6-v2

_qdrant_client_instance = None # Private variable to hold the client instance

def get_qdrant_client() -> QdrantClient:
    global _qdrant_client_instance
    if _qdrant_client_instance is None:
        if not QDRANT_HOST:
            raise ValueError("QDRANT_HOST environment variable not set for Qdrant client.")
        if not QDRANT_API_KEY:
            raise ValueError("QDRANT_API_KEY environment variable not set for Qdrant client.")
        _qdrant_client_instance = QdrantClient(
            url=QDRANT_HOST,
            api_key=QDRANT_API_KEY,
        )
    return _qdrant_client_instance

def create_collection_if_not_exists():
    """Creates the Qdrant collection if it does not already exist."""
    client = get_qdrant_client() # Get client instance
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Collection '{COLLECTION_NAME}' not found, creating...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")

def upsert_vectors(points: list[models.PointStruct]):
    """Inserts or updates vectors in the Qdrant collection."""
    client = get_qdrant_client() # Get client instance
    client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points
    )

def search_vectors(query_vector: list[float], limit: int = 5) -> list[models.ScoredPoint]:
    """Performs a similarity search in the Qdrant collection."""
    client = get_qdrant_client() # Get client instance
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    )
    print(f"DEBUG: Type of response from query_points: {type(response)}")
    print(f"DEBUG: Response from query_points: {response}")
    return response.points if hasattr(response, 'points') else []
