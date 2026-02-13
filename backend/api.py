# run server with - uvicorn api:app --reload
import os
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
from queryfunc import query_rag
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb

load_dotenv()

API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")



client = chromadb.PersistentClient(path="./.chroma")

# create or get a collection
collection = client.get_or_create_collection(
    name="springfield_docs"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    history: list = []

@app.post("/query") # when someone POSTs to /query, run this function
def query(request: QueryRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return query_rag(request.question, request.history)