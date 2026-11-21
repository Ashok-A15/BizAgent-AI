from pathlib import Path
from dotenv import load_dotenv

# load_dotenv() must run before any module that reads env vars is imported
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

from fastapi import FastAPI
from app.database import check_mongo_connection
from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router
from app.routers.agent import router as agent_router
from app.routers.adk import router as adk_router

app = FastAPI(title="BizAgent AI Backend", version="0.1.0")

app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(agent_router)
app.include_router(adk_router)


@app.get("/")
def read_root():
    return {"message": "BizAgent AI backend is running"}


@app.get("/health")
def health_check():
    is_up = check_mongo_connection()
    return {
        "status": "ok",
        "mongodb": "up" if is_up else "down"
    }
