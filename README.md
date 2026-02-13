# Offline RAG Pipeline

Ask questions about your documents using AI that runs entirely on your machine — no cloud, no data leaving your network.

## Overview

A fully offline/air-gapped document Q&A system demonstrating core AI/ML competencies: RAG architecture, vector embeddings, semantic search, and local LLM inference.

Built for environments where data cannot leave the network — defense, government, healthcare, or any privacy-sensitive context.

## Architecture

```
Documents (PDF)
    → PyPDFLoader (extract text)
    → RecursiveCharacterTextSplitter (chunk into passages)
    → OllamaEmbeddings/nomic-embed-text (generate vectors)
    → ChromaDB (store vectors + metadata)

User Query
    → API Key validation
    → Prompt injection detection
    → Embed query (same embedding model)
    → Similarity search (find relevant chunks)
    → Build prompt (inject context)
    → Mistral LLM (generate grounded answer)
    → Return answer + sanitized source citations
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| LLM Inference | Ollama + Mistral | Local language model |
| Embeddings | nomic-embed-text | 768-dim vector generation |
| Vector Store | ChromaDB | Similarity search |
| Orchestration | LangChain | RAG pipeline glue |
| Backend | FastAPI | REST API |
| Frontend | React + TypeScript | Chat interface |

## Requirements

- Python 3.12 (3.14 not supported due to ChromaDB/Pydantic compatibility)
- Node.js 18+
- Ollama installed and running

## Setup

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Start the server
ollama serve

# Pull required models (in a new terminal)
ollama pull mistral
ollama pull nomic-embed-text
```

### 2. Backend Setup

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

Create `backend/.env`:

```
API_KEY=your-secret-key-here
```

Create `frontend/.env`:

```
VITE_API_KEY=your-secret-key-here
```

### 4. Ingest Documents

Place PDF files in `backend/docs/`, then:

```bash
python ingest.py
```

### 5. Start the API

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### 6. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

UI available at `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /query | Ask a question, returns answer + sources |

### Authentication

All endpoints require an `X-API-Key` header:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key-here" \
  -d '{"question": "What is the threat level for Springfield?"}'
```

### Example Response

```json
{
  "answer": "The current threat level for Springfield sector is ELEVATED (Yellow)...",
  "sources": [
    {
      "document": "springfield_briefing.pdf",
      "page": 1
    }
  ]
}
```

## Project Structure

```
offline-rag-pipeline/
├── backend/
│   ├── docs/           # PDF documents to ingest
│   ├── .chroma/        # Vector database storage
│   ├── ingest.py       # Document ingestion pipeline
│   ├── queryfunc.py    # RAG query logic
│   ├── api.py          # FastAPI application
│   ├── .env            # API keys (not committed)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.tsx     # React chat interface
│   ├── .env            # API keys (not committed)
│   └── package.json
└── README.md
```

## Security Features

### API Key Authentication

All API endpoints require a valid `X-API-Key` header. Keys are stored in environment variables and never committed to source control.

```python
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

### Prompt Injection Protection

User inputs are scanned for common injection patterns before being sent to the LLM:

```python
# Blocked patterns include:
- "ignore.*instruction"
- "disregard.*instruction" 
- "print.*document"
- "reveal", "dump", "show.*all"
- "read.*all", "list.*all"
```

Suspicious queries are rejected at the application layer before reaching the model.

### Source Sanitization

Raw document chunks are not returned to the client. Instead, only metadata (document name, page number) is exposed, preventing accidental leakage of sensitive content.

```python
safe_sources = []
for meta in metadatas:
    safe_sources.append({
        "document": meta.get("source", "Unknown"),
        "page": meta.get("page", "N/A")
    })
```

### Defense in Depth

Multiple layers of protection:
1. **Application layer** — Pattern matching blocks obvious attacks
2. **Prompt layer** — System instructions tell LLM to refuse manipulation
3. **Response layer** — Only sanitized metadata returned

## Key Concepts

### Why RAG over Fine-tuning?

- **No training required** — works with any documents immediately
- **Updateable** — add/remove documents without retraining
- **Auditable** — shows source citations for every answer
- **Cost effective** — no GPU training, runs on CPU

### Chunking Strategy

- **500 characters** per chunk with **100 character overlap**
- Overlap prevents losing context at chunk boundaries
- Smaller chunks = more precise retrieval, less context per chunk

### Air-gapped Deployment

- All inference runs locally via Ollama
- No external API calls
- ChromaDB stores vectors on local disk
- Entire system works without internet connectivity

### Conversation Memory

Multi-turn conversations are supported by passing conversation history with each request. The last 3 turns are included in the prompt context, allowing follow-up questions like "Tell me more about that."

## Future Enhancements

- [ ] Document upload via UI
- [ ] Docker containerization
- [ ] Hybrid search (keyword + vector)
- [ ] Retrieval evaluation metrics
- [ ] Role-based access control

## License

MIT