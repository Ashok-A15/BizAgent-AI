import os
from pathlib import Path
from dotenv import load_dotenv

# load_dotenv() must run before any module that reads env vars is imported
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import check_mongo_connection
from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router
from app.routers.agent import router as agent_router
from app.routers.adk import router as adk_router
from app.routers.admin import router as admin_router

app = FastAPI(title="BizAgent AI Backend", version="0.1.0")

cors_env = os.getenv("CORS_ORIGINS", "")
extra_origins = [o.strip() for o in cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        *extra_origins,
    ],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(agent_router)
app.include_router(adk_router)
app.include_router(admin_router)


@app.on_event("startup")
def startup_event():
    try:
        from app.services.vectorstore import add_document, list_documents
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        docs = list_documents()
        if not docs:
            sample_file = Path(__file__).resolve().parent / "sample_docs" / "mysuru_clinic_info.txt"
            if sample_file.exists():
                text = sample_file.read_text(encoding="utf-8")
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_text(text)
                add_document(
                    document_id="mysuru_clinic_01_info",
                    chunks=chunks,
                    metadata={"filename": "mysuru_clinic_info.txt", "business_id": "mysuru_clinic_01"}
                )
    except Exception as e:
        print(f"Startup indexing note: {e}")


@app.get("/")
def read_root():
    return {"message": "BizAgent AI backend is running"}


@app.get("/health")
@app.post("/health")
def health_check():
    is_up = check_mongo_connection()
    return {
        "status": "ok",
        "mongodb": "up" if is_up else "down"
    }
