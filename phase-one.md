Create project root — offline-rag/ with two subdirectories: backend/ and frontend/. Everything Python lives in backend/.
Init Python env — cd backend, create a venv (python3 -m venv venv), activate it. Create a requirements.txt with your initial deps: langchain, langchain-community, chromadb, fastapi, uvicorn, pypdf. Pip install it.
Install Ollama — if you haven't already, grab it from ollama.com.  make sure ollama is running on local machine - ollama serve. Then pull your model: ollama pull llama3.2 and the embedding model: ollama pull nomic-embed-text.
Verify Ollama is running — ollama list should show both models. ollama run llama3.2 "hello" should get a response back.
Write a smoke test script — backend/test_llm.py. Use LangChain's ChatOllama class to send a simple prompt to llama3.2 and print the response. This proves your Python → Ollama connection works. Maybe 10 lines of code.
Write a second smoke test — same file or new one. Use OllamaEmbeddings with nomic-embed-text to embed a short string, print the vector length. This proves your embedding pipeline works.

Init git — from project root, git init, add a .gitignore (venv, __pycache__, .chroma/, node_modules/), make your first commit: feat: project scaffold and ollama verification.