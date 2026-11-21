from typing import List, Dict, Any
from app.services.embeddings import embed_texts
from app.services.vectorstore import get_collection


def retrieve_chunks(
    question: str,
    business_id: str = "default",
    top_k: int = 4,
) -> List[Dict[str, Any]]:
    """Retrieve the top_k most relevant chunks for a question from ChromaDB.

    Args:
        question: The user query string.
        business_id: Business identifier. If not 'default', filters chunks by this ID.
        top_k: Maximum number of nearest chunks to retrieve.

    Returns:
        List of dicts containing text, document_id, filename, business_id, and distance.
    """
    if not question or not question.strip():
        return []

    collection = get_collection()
    total_docs = collection.count()
    if total_docs == 0:
        return []

    # Embed the query using the existing embedding function
    query_embeddings = embed_texts([question.strip()])
    if not query_embeddings:
        return []

    n_results = min(top_k, total_docs)

    query_params: Dict[str, Any] = {
        "query_embeddings": query_embeddings,
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"],
    }

    # Filter by business_id in metadata when business_id is not "default"
    if business_id and business_id != "default":
        query_params["where"] = {"business_id": business_id}

    try:
        results = collection.query(**query_params)
    except Exception:
        # If query fails (e.g. filter matches 0 records), return empty list without crashing
        return []

    documents_list = results.get("documents", [[]])
    metadatas_list = results.get("metadatas", [[]])
    distances_list = results.get("distances", [[]])

    docs = documents_list[0] if documents_list else []
    metas = metadatas_list[0] if metadatas_list else []
    distances = distances_list[0] if distances_list else [0.0] * len(docs)

    chunks: List[Dict[str, Any]] = []
    for doc_text, meta, dist in zip(docs, metas, distances):
        meta_dict = meta or {}
        chunks.append({
            "text": doc_text,
            "document_id": meta_dict.get("document_id", ""),
            "filename": meta_dict.get("filename", ""),
            "business_id": meta_dict.get("business_id", ""),
            "distance": dist,
        })

    return chunks
