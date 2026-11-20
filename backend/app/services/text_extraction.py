import io
from pathlib import Path
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {".txt", ".pdf"}


def extract_text(filename: str, content: bytes) -> str:
    """Extract text from a .txt or .pdf file.

    Args:
        filename: Name of the uploaded file.
        content: Binary content of the file.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If file extension is unsupported or PDF reading fails.
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type '{ext}'. Only .pdf and .txt files are allowed.")

    if ext == ".txt":
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("utf-8", errors="replace")

    if ext == ".pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n".join(pages)
        except Exception as e:
            raise ValueError(f"Failed to read PDF file: {e}") from e

    raise ValueError(f"Unsupported file type '{ext}'.")
