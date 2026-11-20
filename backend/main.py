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

app = FastAPI(title="BizAgent AI Backend", version="0.1.0")


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
