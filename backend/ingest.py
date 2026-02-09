# Write the PDF loader — new file backend/ingest.py. Use LangChain's PyPDFLoader to load your test PDF. 
# Print the raw text to confirm extraction works.

import pprint
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

loader = PyPDFLoader('./docs/springfield_briefing.pdf')
documents = loader.load()

# pprint.pp(documents)

# Add chunking — Use LangChain's RecursiveCharacterTextSplitter. Split your extracted text into chunks 
# (start with ~500 chars, ~100 char overlap). Print how many chunks you get and the first chunk's content.

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# print(f"Total chunks: {len(chunks)}")
# print(f"\nFirst chunk:\n{chunks[0].page_content}")

# Generate embeddings for chunks — Use your OllamaEmbeddings from Phase 1. Embed each chunk. Print one vector length to confirm it's still 768.

embeddings = OllamaEmbeddings(model="nomic-embed-text")

ids = []
documents = []
vectors = []
metadatas = []

for i, chunk in enumerate(chunks):
    ids.append(f"chunk_{i}")
    documents.append(chunk.page_content)
    vectors.append(embeddings.embed_query(chunk.page_content)) # takes the string (chunk) and makes the vector 
    metadatas.append(chunk.metadata)


# Store in ChromaDB — Create a Chroma collection, 
# add your chunks with their embeddings. 
# Use persist_directory so it saves to disk 
# (e.g., backend/.chroma/). 
# Print the collection count to confirm storage.

# Create a client with persistence (saves to disk)
client = chromadb.PersistentClient(path="./.chroma")

# create or get a collection
collection = client.get_or_create_collection(
    name="springfield_docs"
)

# add chunks to chroma (chroma needs: ids, documents, embeddings)
collection.add(
    ids=ids, # unique IDs
    documents=documents, # original text
    embeddings=vectors, # our 768-dim vectors
    metadatas=metadatas # source/page info
)

print(f"Stored {collection.count()} chunks")

# Test retrival, query by similarity

query = "Who is Homer Simpson?"
query_vector = embeddings.embed_query(query)

results = collection.query(
    query_embeddings=[query_vector], # your question as a vector
    n_results=3 # top 3 matches
)

print(f"\nQuery: {query}")
print(f"Top results:")
for i, doc in enumerate(results['documents'][0]):
    print(f"\n--- Result {i+1} ---")
    print(doc)

# your query vector might be [0.12, -0.45, 0.78, 0.33, ...] (768 total).
# And each stored chunk has its own 768-number vector like [0.11, -0.44, 0.80, 0.31, ...].
# Chroma compares the query vector against every stored vector using math (cosine similarity or distance) to find which ones "point in the same direction" — meaning similar meaning.
# The closer the numbers match across all 768 dimensions, the more semantically similar the texts are. That's how "Who is Homer Simpson?" finds chunks that mention Homer even if they don't use those exact words.
