"""
Verification script to check if ingestion was successful.
Run this after ingestion.py completes.
"""
import asyncio
from utils.qdrant_client import get_qdrant_client, COLLECTION_NAME
from utils.postgres_client import AsyncSessionLocal, ChunkMetadata
from utils.openai_client import get_embedding
from sqlalchemy import select, func

async def verify_ingestion():
    print("=" * 60)
    print("RAG CHATBOT INGESTION VERIFICATION")
    print("=" * 60)

    # 1. Check Qdrant Collection
    print("\n[1] Checking Qdrant Vector Database...")
    try:
        client = get_qdrant_client()
        collection_info = client.get_collection(COLLECTION_NAME)

        # Handle different Qdrant client versions
        vectors_count = getattr(collection_info, 'vectors_count', None)
        points_count = getattr(collection_info, 'points_count', None)

        # For newer versions, use vectors_config
        if vectors_count is None and hasattr(collection_info, 'vectors_config'):
            vectors_count = collection_info.vectors_config.get('size', 'Unknown')
            points_count = 'Check manually'

        print(f"[OK] Collection Name: {COLLECTION_NAME}")
        print(f"[OK] Collection exists and is accessible")

        # Try to count points using scroll
        try:
            scroll_result = client.scroll(collection_name=COLLECTION_NAME, limit=1)
            if scroll_result and len(scroll_result) > 0:
                points_count = len(scroll_result[0]) if isinstance(scroll_result, tuple) else len(scroll_result)
                print(f"[OK] Collection has data (sampled {points_count} points)")
            else:
                print("[WARNING] Could not verify point count")
        except:
            print("[INFO] Using collection info for verification")

        print(f"[OK] SUCCESS: Qdrant collection is configured correctly")
    except Exception as e:
        print(f"[ERROR] Could not connect to Qdrant: {e}")
        return False

    # 2. Check PostgreSQL Database
    print("\n[2] Checking PostgreSQL Metadata Database...")
    try:
        async with AsyncSessionLocal() as session:
            # Count total chunks
            result = await session.execute(select(func.count(ChunkMetadata.id)))
            chunk_count = result.scalar()

            print(f"[OK] Total Chunks in PostgreSQL: {chunk_count}")

            if chunk_count == 0:
                print("[WARNING] No chunks found! Ingestion may have failed.")
                return False

            # Get sample chunks
            result = await session.execute(select(ChunkMetadata).limit(3))
            sample_chunks = result.scalars().all()

            print(f"\n[INFO] Sample Chunks:")
            for i, chunk in enumerate(sample_chunks, 1):
                print(f"\n  Chunk {i}:")
                print(f"    ID: {chunk.id}")
                print(f"    Source URL: {chunk.source_url}")
                print(f"    Content Preview: {chunk.content[:100]}...")

            # Check unique source URLs
            result = await session.execute(select(func.count(func.distinct(ChunkMetadata.source_url))))
            unique_sources = result.scalar()
            print(f"\n[OK] Unique Source Documents: {unique_sources}")

            print(f"[OK] SUCCESS: {chunk_count} chunks stored in PostgreSQL")
    except Exception as e:
        print(f"❌ ERROR: Could not connect to PostgreSQL: {e}")
        return False

    # 3. Test Vector Search
    print("\n[3] Testing Vector Search...")
    try:
        test_query = "What is physical AI?"
        print(f"   Query: '{test_query}'")

        # Generate embedding for test query
        query_embedding = get_embedding(test_query)
        print(f"[OK] Generated query embedding: {len(query_embedding)} dimensions")

        # Search Qdrant
        from utils.qdrant_client import search_vectors
        hits = search_vectors(query_embedding, limit=3)

        if not hits:
            print("[WARNING] No search results found!")
            return False

        print(f"[OK] Found {len(hits)} relevant chunks")
        print("\n[INFO] Top Search Results:")
        for i, hit in enumerate(hits, 1):
            score = hit.score if hasattr(hit, 'score') else 'N/A'
            chunk_id = hit.payload.get('chunk_id', 'N/A') if hasattr(hit, 'payload') else 'N/A'
            print(f"   {i}. Score: {score}, Chunk ID: {chunk_id[:8]}...")

        print("[OK] SUCCESS: Vector search is working!")
    except Exception as e:
        print(f"[ERROR] Vector search failed: {e}")
        return False

    # 4. Test Full RAG Pipeline
    print("\n[4] Testing Full RAG Pipeline...")
    try:
        # Get chunk IDs from search results
        chunk_ids = [hit.payload["chunk_id"] for hit in hits if "chunk_id" in hit.payload]

        if not chunk_ids:
            print("[WARNING] No chunk IDs found in search results!")
            return False

        # Retrieve full content from PostgreSQL
        from utils.postgres_client import get_chunks_by_ids
        chunks_metadata = await get_chunks_by_ids(chunk_ids)

        if not chunks_metadata:
            print("[WARNING] Could not retrieve chunk metadata!")
            return False

        print(f"[OK] Retrieved {len(chunks_metadata)} chunks from PostgreSQL")
        print("\n[INFO] Sample Retrieved Content:")
        for i, chunk in enumerate(chunks_metadata[:2], 1):
            print(f"\n   Chunk {i}:")
            print(f"   Source: {chunk.source_url}")
            print(f"   Content: {chunk.content[:150]}...")

        print("\n[OK] SUCCESS: Full RAG pipeline is working!")
    except Exception as e:
        print(f"[ERROR] RAG pipeline test failed: {e}")
        return False

    # 5. Final Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"[OK] Qdrant Collection: Verified")
    print(f"[OK] PostgreSQL Chunks: {chunk_count}")
    print(f"[OK] Unique Documents: {unique_sources}")
    print(f"[OK] Vector Search: Working")
    print(f"[OK] RAG Pipeline: Working")
    print("\n[SUCCESS] ALL CHECKS PASSED! Your chatbot is ready to use!")
    print("=" * 60)

    print("\n[NEXT STEPS]:")
    print("1. Start the FastAPI server: uvicorn main:app --reload --port 8000")
    print("2. Test the /chat endpoint")
    print("3. Or start the frontend: npm start")

    return True

if __name__ == "__main__":
    result = asyncio.run(verify_ingestion())
    exit(0 if result else 1)
