import faiss
import pickle
import numpy as np
from ollama import embeddings, chat

INDEX_FILE = "faiss_index"
DOCS_FILE = "docs.pkl"

# Load FAISS + docs
index = faiss.read_index(INDEX_FILE)
with open(DOCS_FILE, "rb") as f:
    docs = pickle.load(f)

# Ask a question
question = input("Ask a question: ")

# Embed the question
q_emb = embeddings(model="nomic-embed-text", prompt=question)["embedding"]
q_emb = np.array([q_emb]).astype("float32")

# Search in FAISS
D, I = index.search(q_emb, k=3)
retrieved = [docs[i] for i in I[0]]


# Ask Ollama
prompt = f"Answer the question using this context:\n\n{retrieved}\n\nQuestion: {question}"
answer = chat(model="llama2", messages=[{"role":"user", "content":prompt}])
print("\n🤖 Ollama Answer:", answer["message"]["content"])
