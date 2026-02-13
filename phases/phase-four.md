Phase 4 — API Layer with FastAPI
Here's your roadmap:
Install FastAPI and Uvicorn — pip install fastapi uvicorn
Create backend/api.py — This will be your API server
Move your query logic into a function (queryfunc.py) — Something like def query_rag(question: str) -> dict
Create a POST endpoint (api.py) — /query that accepts a question and returns the answer + sources
Initialize ChromaDB and models once at startup — Not on every request


Run the server — uvicorn api:app --reload
Test it — Hit http://localhost:8000/docs for the interactive Swagger UI
Commit — feat: FastAPI endpoint for RAG queries