from typing import List, Dict, Any
import google.generativeai as genai
from app.config import GEMINI_API_KEY

CHAT_MODEL_NAME = "gemini-3.6-flash"
SYSTEM_INSTRUCTION = (
    "Answer ONLY from the context below. If the answer is not in the context, "
    "say 'I don't know based on the documents provided.' Do not invent facts. "
    "Quote the source filename for each fact you use."
)
DEFAULT_UNKNOWN_ANSWER = "I don't know based on the documents provided."


def answer_question(question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Answer a user question strictly using the provided context chunks.

    Args:
        question: User query string.
        chunks: List of retrieved chunk dicts.

    Returns:
        Dict with 'answer' and 'sources' (list of distinct {document_id, filename}).
    """
    if not chunks:
        return {
            "answer": DEFAULT_UNKNOWN_ANSWER,
            "sources": [],
        }

    # Ensure genai is configured with the key from config
    genai.configure(api_key=GEMINI_API_KEY)

    # Build context from chunks with their source filenames
    context_blocks = []
    for chunk in chunks:
        filename = chunk.get("filename", "unknown")
        text = chunk.get("text", "")
        context_blocks.append(f"Source [{filename}]:\n{text}")

    context_text = "\n\n".join(context_blocks)

    prompt = f"""Context:
{context_text}

Question:
{question}

Answer:"""

    model = genai.GenerativeModel(
        model_name=CHAT_MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION,
    )

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip() if response.text else DEFAULT_UNKNOWN_ANSWER
    except Exception as e:
        raise RuntimeError(f"Gemini generateContent error: {e}") from e

    # Build distinct sources from chunks used
    seen_sources = set()
    sources = []
    # If the answer indicates unknown information, no sources were used
    if DEFAULT_UNKNOWN_ANSWER.lower() in answer.lower():
        sources = []
    else:
        for chunk in chunks:
            doc_id = chunk.get("document_id", "")
            fname = chunk.get("filename", "")
            key = (doc_id, fname)
            if key not in seen_sources and doc_id:
                seen_sources.add(key)
                sources.append({"document_id": doc_id, "filename": fname})

    return {
        "answer": answer,
        "sources": sources,
    }
