import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "chatbot_knowledge")

if not QDRANT_HOST:
    raise ValueError("QDRANT_HOST environment variable not set.")
if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY environment variable not set.")

qdrant_client = QdrantClient(
    url=QDRANT_HOST, # Using url as per previous fix
    api_key=QDRANT_API_KEY,
)

print(f"Attempting to delete Qdrant collection: {COLLECTION_NAME}")
try:
    qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' deleted successfully.")
except Exception as e:
    print(f"Error deleting collection '{COLLECTION_NAME}': {e}")
    print("It might not have existed or there was an access issue.")

print("Please run the ingestion script (python ingestion.py) next.")