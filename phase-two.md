Phase 2 — Document Ingestion Pipeline

Create a test PDF — drop any small PDF into backend/docs/ folder. Could be a random manual, a one-pager you create, whatever. Just need something to test with.
Write the PDF loader — new file backend/ingest.py. Use LangChain's PyPDFLoader to load your test PDF. Print the raw text to confirm extraction works.
Add chunking — Use LangChain's RecursiveCharacterTextSplitter. Split your extracted text into chunks (start with ~500 chars, ~100 char overlap). Print how many chunks you get and the first chunk's content.
Generate embeddings for chunks — Use your OllamaEmbeddings from Phase 1. Embed each chunk. Print one vector length to confirm it's still 768.

Store in ChromaDB — Create a Chroma collection, add your chunks with their embeddings. Use persist_directory so it saves to disk (e.g., backend/.chroma/). Print the collection count to confirm storage.

Test retrieval — Write a simple query against your collection. Use similarity_search with a question related to your PDF content. Print the top result. If it returns relevant text, your ingestion pipeline works.
Commit — feat: document ingestion pipeline with chunking and vector storage