# This will be your main query script, separate from ingestion.

# Load existing ChromaDB collection — Use PersistentClient with same path, get_collection instead of get_or_create_collection.

import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter




client = chromadb.PersistentClient(path="./.chroma")

collection = client.get_collection(
    name="springfield_docs"
)

# Get user query — Start with a hardcoded question like "What is the threat level for Springfield?"

# query = "What is the threat level for Springfield?"

# Embed the query — Use OllamaEmbeddings to convert question to vector.

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# query_vector = embeddings.embed_query(query)

# Retrieve relevant chunks — Query ChromaDB for top 3-5 similar chunks.

# results = collection.query(
#     query_embeddings=[query_vector], # your question as a vector
#     n_results=3 # top 3 matches
# )

# print(f"\nQuery: {query}")
# print(f"Top results:")
# for i, doc in enumerate(results['documents'][0]):
#     print(f"\n--- Result {i+1} ---")
#     print(doc)

# Build the prompt — Combine a system instruction + retrieved chunks + user question into one prompt. Something like:

#    You are an intelligence analyst. Use only the following context to answer the question. Cite your sources.
   
#    Context:
#    {chunks go here}
   
#    Question: {user question}

# Send to LLM — Use ChatOllama to get a response.
# Print answer with sources — Show the LLM's response and which chunks it used.
# Test with a few different questions — Make sure it gives grounded answers, not hallucinations.

model = ChatOllama(model="llama3.2", temperature=0)

new_query = 'Whom is the most dangerous person in Springfield?'

#embeddings declared above

new_query_vector = embeddings.embed_query(new_query)

new_query_results = collection.query(
    query_embeddings=[new_query_vector], # your question as a vector
    n_results=3 # top 3 matches
)

# Extract the text from new_query_results
retrieved_chunks = new_query_results['documents'][0]

# print(f"\nQuery: {new_query}")
# print(f"Top results:")
# for i, doc in enumerate(new_query_results['documents'][0]):
#     print(f"\n--- Result {i+1} ---")
#     print(doc)

# Build the context string - formatting
context = "\n\n".join(retrieved_chunks)
# produces this
# """
# Chunk one text here
#
# Chunk two text here
#
# Chunk three text here
# """

# Build prompt with the retrieved context baked in
prompt = f"""You are an intelligence analyst. Use only the following context to answer the question. Cite your sources.

Context:
{context}

Question: Who is the greatest threat in Springfield?"""

# Send to LLM
messages = [("human", prompt)]
response = model.invoke(messages)

print('LLM response:', response.content)
print("\n--- Sources used ---")
for i, chunk in enumerate(retrieved_chunks):
    print(f"\nChunk {i+1}: {chunk[:100]}...")