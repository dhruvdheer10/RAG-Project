import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from chunk_texts import load_and_chunk_documents

# Parameters
INPUT_DIR = "final_texts"
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "vector_index/faiss_index"
METADATA_PATH = "vector_index/chunk_metadata.pkl"

# Load local embedding model
model = SentenceTransformer(MODEL_NAME)

# Load and chunk text files
chunks = load_and_chunk_documents(Path(INPUT_DIR))
texts = [chunk[1] for chunk in chunks]
metadata = [chunk[0] for chunk in chunks]

# Generate embeddings
print(f"📦 Generating embeddings for {len(texts)} chunks...")
vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# Build and save FAISS index
dim = vectors.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(vectors)

os.makedirs("vector_index", exist_ok=True)
faiss.write_index(index, INDEX_PATH)

# Save chunk metadata (text + IDs)
with open(METADATA_PATH, "wb") as f:
    pickle.dump(list(zip(metadata, texts)), f)

print(f"\n✅ Saved FAISS index: {INDEX_PATH}")
print(f"📝 Saved metadata: {METADATA_PATH}")
