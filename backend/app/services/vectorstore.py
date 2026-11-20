from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
from app.services.embeddings import embed_texts

CHROMA_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "chromadb_data"
CHROMA_DATA_PATH.mkdir(parents=True, exist_ok=True)
COLLECTION_NAME = "bizagent_docs"


class GeminiEmbeddingFunction(EmbeddingFunction[Documents]):
    """Custom ChromaDB embedding function delegating to embed_texts."""

    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        return embed_texts(list(input))


_embedding_function = GeminiEmbeddingFunction()
_chroma_client: Optional[chromadb.PersistentClient] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Return singleton chromadb PersistentClient."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DATA_PATH))
    return _chroma_client


def get_collection():
    """Return the bizagent_docs collection with Gemini embedding function."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_function,
    )


def add_document(document_id: str, chunks: List[str], metadata: Dict[str, Any]) -> None:
    """Add chunked document and its metadata to ChromaDB.

    Args:
        document_id: Unique identifier for the document.
        chunks: List of text chunk strings.
        metadata: Document-level metadata dict.
    """
    if not chunks:
        return

    collection = get_collection()
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            **metadata,
            "document_id": document_id,
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )


def list_documents() -> List[Dict[str, Any]]:
    """List distinct document records with filename and chunk count from collection metadata.

    Returns:
        List of dicts containing document_id, filename, business_id, and chunk_count.
    """
    collection = get_collection()
    data = collection.get(include=["metadatas"])
    metadatas = data.get("metadatas", []) or []

    docs_map: Dict[str, Dict[str, Any]] = {}
    for meta in metadatas:
        if not meta or "document_id" not in meta:
            continue
        doc_id = str(meta["document_id"])
        if doc_id not in docs_map:
            docs_map[doc_id] = {
                "document_id": doc_id,
                "filename": meta.get("filename", "unknown"),
                "business_id": meta.get("business_id", "default"),
                "chunk_count": 0,
            }
        docs_map[doc_id]["chunk_count"] += 1

    return list(docs_map.values())
