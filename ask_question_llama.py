from llama_cpp import Llama
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Config
MODEL_PATH = "models/mistral-7b/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
INDEX_PATH = "vector_index/faiss_index"
METADATA_PATH = "vector_index/chunk_metadata.pkl"
TOP_K = 5

# Load FAISS index + metadata
index = faiss.read_index(INDEX_PATH)
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load LLaMA
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=4)

# Ask user
question = input("❓ Ask a question about the training content:\n> ")

# Embed question and search
q_vec = embedder.encode([question], convert_to_numpy=True)
_, I = index.search(q_vec, TOP_K)
retrieved_chunks = [metadata[i][1] for i in I[0]]

context = "\n\n---\n\n".join(retrieved_chunks)

# Prompt format (Mistral-style)
prompt = f"""<s>[INST] Use the following training content to answer the question.

Training Content:
{context}

Question: {question}
[/INST]"""

# Run inference
response = llm(prompt, max_tokens=512, stop=["</s>"])
print("\n💡 Answer:")
print(response["choices"][0]["text"].strip())
