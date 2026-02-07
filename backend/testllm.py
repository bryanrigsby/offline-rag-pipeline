# Write a smoke test script — backend/test_llm.py. Use LangChain's ChatOllama class to send a simple prompt to llama3.2
# and print the response. This proves your Python → Ollama connection works. Maybe 10 lines of code.

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

model = ChatOllama(model="llama3.2")

messages = [
    (
        "system", "You are a helpful assistant named Percy."
    ),
    (
        "human", "What is your name?"
    )
]

response = model.invoke(messages)

print(response.content)


# Write a second smoke test — same file or new one. Use OllamaEmbeddings with nomic-embed-text to embed a short string, 
# print the vector length. This proves your embedding pipeline works.

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector = embeddings.embed_query("Hello, how are you?")

print(len(vector))