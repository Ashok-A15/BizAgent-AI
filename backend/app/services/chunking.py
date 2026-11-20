from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)


def chunk_text(text: str) -> List[str]:
    """Split text into chunks using RecursiveCharacterTextSplitter.

    Args:
        text: Raw text string to split.

    Returns:
        List of text chunks.
    """
    if not text:
        return []
    return _splitter.split_text(text)
