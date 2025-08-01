import streamlit as st
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# Configs
MODEL_PATH = "models/mistral-7b/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
INDEX_PATH = "vector_index/faiss_index"
METADATA_PATH = "vector_index/chunk_metadata.pkl"
TOP_K = 4

# Load once
@st.cache_resource
def load_everything():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
    llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=4)
    return embedder, index, metadata, llm

embedder, index, metadata, llm = load_everything()

# UI
st.set_page_config(page_title="CSC RAG Chatbot", layout="wide")
st.title("💬 CSC Training Chatbot (Local + Private)")

user_question = st.text_input("Ask a question about ticketing:", "")

if user_question:
    # Embed + retrieve chunks
    q_vec = embedder.encode([user_question], convert_to_numpy=True)
    _, I = index.search(q_vec, TOP_K)
    retrieved_chunks = [metadata[i][1] for i in I[0]]
    context = "\n\n---\n\n".join(retrieved_chunks)

    # Format prompt for Mistral
    prompt = f"""<s>[INST] Use the following training content to answer the question.

Training Content:
{context}

Question: {user_question}
[/INST]"""

    with st.spinner("Thinking..."):
        res = llm(prompt, max_tokens=512, stop=["</s>"])
        answer = res["choices"][0]["text"].strip()

    # Show answer
    st.success("💡 Answer:")
    st.markdown(answer)

    # Optionally show retrieved chunks
    with st.expander("🧾 View retrieved context"):
        for idx, chunk in enumerate(retrieved_chunks):
            st.markdown(f"**Chunk {idx+1}:**\n\n{chunk}\n\n---")

