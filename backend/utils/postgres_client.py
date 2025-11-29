import os
import uuid
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.sql import select 
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qs # Import urlparse utilities

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- Connection URL and SSL Handling for asyncpg ---
connect_args = {}
if DATABASE_URL:
    parsed_url = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed_url.query)

    # Handle SSL mode
    if "sslmode" in query_params and query_params["sslmode"][0] == "require":
        connect_args["ssl"] = True
    
    # Rebuild the DATABASE_URL without query parameters for asyncpg
    # as asyncpg expects a clean DSN (Data Source Name)
    clean_dsn = urlunparse(parsed_url._replace(query="", params="", fragment=""))
    DATABASE_URL = clean_dsn

Base = declarative_base()

class ChunkMetadata(Base):
    __tablename__ = "chunk_metadata"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    source_url = Column(String, nullable=False)
    page_number = Column(Integer, nullable=True)
    start_char = Column(Integer, nullable=True)
    end_char = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ChunkMetadata(id='{self.id}', source_url='{self.source_url}')>"

# Async Engine
engine = create_async_engine(DATABASE_URL, echo=True, connect_args=connect_args)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_chunk_metadata(chunk_data: dict) -> ChunkMetadata:
    async with AsyncSessionLocal() as session:
        chunk = ChunkMetadata(**chunk_data)
        session.add(chunk)
        await session.commit()
        await session.refresh(chunk)
        return chunk

async def bulk_insert_chunk_metadata(chunks_data: list[dict]) -> list[ChunkMetadata]:
    async with AsyncSessionLocal() as session:
        chunks = [ChunkMetadata(**data) for data in chunks_data]
        session.add_all(chunks)
        await session.commit()
        for chunk in chunks:
            await session.refresh(chunk)
        return chunks

async def get_chunk_metadata(chunk_id: str) -> Optional[ChunkMetadata]:
    async with AsyncSessionLocal() as session:
        return await session.get(ChunkMetadata, chunk_id)

async def get_chunks_by_ids(chunk_ids: list[str]) -> list[ChunkMetadata]:
    async with AsyncSessionLocal() as session:
        # Correctly query for multiple IDs
        result = await session.execute(select(ChunkMetadata).where(ChunkMetadata.id.in_(chunk_ids)))
        return result.scalars().all()

# This needs to be imported from sqlalchemy.sql for select to work
from sqlalchemy.sql import select
