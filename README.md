# BizAgent AI

BizAgent AI is an AI agent platform for small businesses that enables customers to interact with an AI assistant grounded strictly in business documents. The agent assists with answering inquiries via RAG, booking appointments, creating support tickets, and capturing customer leads.

## Tech Stack

- **Backend**: FastAPI, Python 3.13
- **Database & Storage**: MongoDB, ChromaDB
- **AI & Orchestration**: Google Gemini, LangChain
- **Frontend**: React (planned)
- **Deployment & Infra**: Docker, AWS (planned)

## Getting Started

### 1. Prerequisites
- Python 3.13 installed
- MongoDB (running locally or MongoDB Atlas)

### 2. Virtual Environment Setup
```bash
# Create virtual environment with Python 3.13
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Environment Variables
Copy `.env.example` to `.env` inside the `backend` directory:
```bash
cp backend/.env.example backend/.env
```
Configure your environment variables in `backend/.env`.

### 5. Run the Server
From the `backend/` directory:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Access the API:
- Root endpoint: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Documents upload: http://127.0.0.1:8000/api/documents/upload
- Documents list: http://127.0.0.1:8000/api/documents
- RAG chat: http://127.0.0.1:8000/api/chat
- Agent tool chat: http://127.0.0.1:8000/api/agent/chat
- Swagger API documentation: http://127.0.0.1:8000/docs

## Project Status

- **Day 1**: Initial backend skeleton setup complete (FastAPI app, MongoDB connection helper, Pydantic data models, pinned dependencies).
- **Day 2**: Document upload, text extraction (.pdf & .txt), RecursiveCharacterTextSplitter chunking, Gemini embeddings (models/gemini-embedding-001), and ChromaDB persistent vector storage setup complete.
- **Day 3**: RAG chat endpoint (/api/chat) with Gemini (gemini-3.6-flash) grounded strictly in uploaded documents with citations.
- **Day 4**: Agent tool calling (/api/agent/chat) with intelligent intent routing (book appointment, create ticket, save lead) persisting directly to MongoDB.
- Protocol/toolkit enhancements (MCP, Google ADK), React frontend, Docker containerization, and AWS deployment are planned for subsequent phases.
