from typing import List
import google.generativeai as genai
from app.config import GEMINI_API_KEY


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using Google Gemini models/gemini-embedding-001 in batches of 10.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (List[List[float]]).

    Raises:
        Exception: If the Gemini API call fails (no fallback).
    """
    if not texts:
        return []

    # Configure API key from config, never hardcoded
    genai.configure(api_key=GEMINI_API_KEY)

    embeddings: List[List[float]] = []
    batch_size = 10

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = genai.embed_content(
            model="models/gemini-embedding-001",
            content=batch,
        )
        batch_embeddings = response.get("embedding", [])
        embeddings.extend(batch_embeddings)

    return embeddings
