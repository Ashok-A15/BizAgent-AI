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

### 5. Run the Application

#### Option A: Run with Docker (Recommended)
Build and run both backend and frontend with a single command:
```bash
docker compose up --build
```
Or run in detached mode:
```bash
docker compose up --build -d
```
Access the application:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health

Stop containers:
```bash
docker compose down
```

#### Option B: Run Locally

##### Run the Backend Server
From the `backend/` directory:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

##### Run the Frontend
From the `frontend/` directory:
```bash
cd frontend
npm install
npm run dev
```
The React frontend will be available at: http://localhost:5173 (with dev server proxy to backend on port 8000).

Access the API:
- Root endpoint: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Documents upload: http://127.0.0.1:8000/api/documents/upload
- Documents list: http://127.0.0.1:8000/api/documents
- RAG chat: http://127.0.0.1:8000/api/chat
- Agent tool chat: http://127.0.0.1:8000/api/agent/chat
- ADK agent chat: http://127.0.0.1:8000/api/adk/chat
- Admin tickets: http://127.0.0.1:8000/api/admin/tickets
- Admin appointments: http://127.0.0.1:8000/api/admin/appointments
- Admin leads: http://127.0.0.1:8000/api/admin/leads
- Swagger API documentation: http://127.0.0.1:8000/docs

MCP Server:
- Stdio transport: `python backend/mcp_server.py`

## Project Status

- **Day 1**: Initial backend skeleton setup complete (FastAPI app, MongoDB connection helper, Pydantic data models, pinned dependencies).
- **Day 2**: Document upload, text extraction (.pdf & .txt), RecursiveCharacterTextSplitter chunking, Gemini embeddings (`models/gemini-embedding-001`), and ChromaDB persistent vector storage setup complete.
- **Day 3**: RAG chat endpoint (`/api/chat`) with Gemini (`gemini-3.6-flash`) grounded strictly in uploaded documents with citations.
- **Day 4**: Agent tool calling (`/api/agent/chat`) with intent routing (book appointment, create ticket, save lead) persisting directly to MongoDB.
- **Day 4b**: FastMCP server (`backend/mcp_server.py`) exposing 4 tools (`search_documents`, `book_appointment`, `create_ticket`, `save_lead`) over stdio transport + Google ADK agent (`gemini-3.6-flash`) integrated with Runner and InMemorySessionService, accessible via `POST /api/adk/chat`.
- **Day 5**: React frontend (Vite) with 3 pages (Customer Chat, Upload Documents, Admin Dashboard), FastAPI CORS middleware, and admin list endpoints (`GET /api/admin/tickets`, `GET /api/admin/appointments`, `GET /api/admin/leads`).
- **Day 6**: Docker containerization — backend (`python:3.13-slim`), multi-stage frontend build with Nginx (`node:22-alpine` -> `nginx:alpine`), and Docker Compose orchestration (`docker compose up --build`).
- AWS and Vercel deployments are planned for Day 7.
