"""
Interview Ace — RAG (Retrieval-Augmented Generation)

Handles document ingestion, chunking, embedding, and retrieval.

Architecture:
    Document Upload
        → Text Extraction (PDF/DOCX/TXT)
        → Chunking (RecursiveCharacterTextSplitter, 512 tokens, 50 overlap)
        → Embedding (sentence-transformers / all-MiniLM-L6-v2)
        → Storage (ChromaDB)

    Query Time
        → Embed query
        → Similarity search (top-k)
        → Return relevant chunks
"""

from pathlib import Path
from loguru import logger


class RAGEngine:
    """Manages the document retrieval pipeline."""

    def __init__(self, persist_dir: str = "./data/chromadb", collection_name: str = "interview_kb"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self._client = None
        self._collection = None

    async def initialize(self):
        """Initialize ChromaDB and load existing collection."""
        # TODO:
        # import chromadb
        # self._client = chromadb.PersistentClient(path=self.persist_dir)
        # self._collection = self._client.get_or_create_collection(
        #     name=self.collection_name,
        #     metadata={"hnsw:space": "cosine"},
        # )
        logger.info(f"📚 RAG Engine initialized (dir={self.persist_dir})")

    async def ingest_document(self, text: str, metadata: dict = None) -> int:
        """Chunk, embed, and store a document.

        Args:
            text: Full document text
            metadata: Optional metadata (filename, source, etc.)

        Returns:
            Number of chunks created
        """
        # Step 1: Chunk text
        chunks = self._chunk_text(text)

        # Step 2: Embed and store
        # for i, chunk in enumerate(chunks):
        #     self._collection.add(
        #         documents=[chunk],
        #         metadatas=[{**(metadata or {}), "chunk_index": i}],
        #         ids=[f"{metadata.get('filename', 'doc')}_chunk_{i}"],
        #     )

        logger.info(f"📄 Ingested document: {len(chunks)} chunks")
        return len(chunks)

    async def query(self, query_text: str, top_k: int = 5) -> list[dict]:
        """Retrieve the most relevant chunks for a query.

        Args:
            query_text: The search query (e.g., interview question)
            top_k: Number of results to return

        Returns:
            List of dicts with keys: text, metadata, score
        """
        # TODO:
        # results = self._collection.query(
        #     query_texts=[query_text],
        #     n_results=top_k,
        # )
        # return [
        #     {"text": doc, "metadata": meta, "score": score}
        #     for doc, meta, score in zip(
        #         results["documents"][0],
        #         results["metadatas"][0],
        #         results["distances"][0],
        #     )
        # ]
        return []

    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
        """Split text into overlapping chunks.

        Uses a simple word-based splitter. For production, consider
        RecursiveCharacterTextSplitter from langchain or custom logic.
        """
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - overlap
        return chunks
