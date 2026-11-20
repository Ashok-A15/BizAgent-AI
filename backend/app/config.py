import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure environment variables are loaded
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bizagent_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
