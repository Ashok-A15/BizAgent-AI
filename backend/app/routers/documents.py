import uuid
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.services.text_extraction import extract_text
from app.services.chunking import chunk_text
from app.services.vectorstore import add_document, list_documents
from app.database import check_mongo_connection

router = APIRouter(prefix="/api/documents", tags=["documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".txt", ".pdf"}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    business_id: str = Form(default="default"),
):
    """Upload a .pdf or .txt document, extract text, chunk, embed, and store in ChromaDB."""
    filename = file.filename or ""
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Only .pdf and .txt files are allowed.",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum allowed size of 10 MB.",
        )

    try:
        text = extract_text(filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Uploaded file contains no extractable text.",
        )

    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="Failed to generate chunks from the uploaded document.",
        )

    doc_id = str(uuid.uuid4())
    metadata = {
        "filename": filename,
        "business_id": business_id,
    }

    try:
        add_document(document_id=doc_id, chunks=chunks, metadata=metadata)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error embedding or storing document in vector store: {str(e)}",
        )

    is_mongo_up = check_mongo_connection()
    mongo_status = "up" if is_mongo_up else "down"

    return {
        "document_id": doc_id,
        "filename": filename,
        "business_id": business_id,
        "characters": len(text),
        "chunks": len(chunks),
        "mongodb": mongo_status,
    }


@router.get("")
@router.get("/")
def get_documents():
    """Retrieve distinct documents stored in vector store."""
    docs = list_documents()
    return {"documents": docs}
