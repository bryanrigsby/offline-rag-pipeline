Phase 3 — RAG Query Pipeline

Create backend/query.py — This will be your main query script, separate from ingestion.
Load existing ChromaDB collection — Use PersistentClient with same path, get_collection instead of get_or_create_collection.
Get user query — Start with a hardcoded question like "What is the threat level for Springfield?"
Embed the query — Use OllamaEmbeddings to convert question to vector.
Retrieve relevant chunks — Query ChromaDB for top 3-5 similar chunks.

Build the prompt — Combine a system instruction + retrieved chunks + user question into one prompt. Something like:

   You are an intelligence analyst. Use only the following context to answer the question. Cite your sources.
   
   Context:
   {chunks go here}
   
   Question: {user question}

Send to LLM — Use ChatOllama to get a response.
Print answer with sources — Show the LLM's response and which chunks it used.
Test with a few different questions — Make sure it gives grounded answers, not hallucinations.
Commit — feat: RAG query pipeline with context injection

Start with steps 1-5, get retrieval working first. Then we'll add the LLM part.