import os
from pathlib import Path
from typing import List, Tuple

# Parameters for chunking
CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 100
INPUT_DIR = Path("final_texts")

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def load_and_chunk_documents(input_dir: Path) -> List[Tuple[str, str]]:
    all_chunks = []
    for file_path in input_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            all_chunks.append((f"{file_path.name}_chunk_{i}", chunk))
    return all_chunks

if __name__ == "__main__":
    chunks = load_and_chunk_documents(INPUT_DIR)
    print(f"✅ Total chunks created: {len(chunks)}")
    print(f"📌 Example chunk:\n\n{chunks[0][1][:500]}...")
