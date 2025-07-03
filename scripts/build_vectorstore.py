# scripts/build_vectorstore.py
"""
Script to build a FAISS vector store from precomputed embeddings and save the index to disk.
Assumes embeddings are saved in data/embeddings/embeddings_<model_name>.npz
"""
import os
import numpy as np
import faiss
from pathlib import Path

# 1) Chemin vers la racine du projet (= dossier chatbot_rag/)
BASE_DIR = Path(__file__).resolve().parents[3]

# 2) Chemin vers data/, embeddings/ et vectorstore/
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"


# Create index_dir if it doesn't exist
index_dir.mkdir(parents=True, exist_ok=True)

# Find embeddings file
emb_files = list(embeddings_dir.glob("embeddings_*.npz"))
if not emb_files:
    raise FileNotFoundError(f"No embeddings file found in {embeddings_dir}")
emb_path = emb_files[0]
print(f"Loading embeddings from {emb_path}")

# Load embeddings
data = np.load(emb_path)
embeddings = data['embeddings'].astype('float32')

# Build FAISS index (Flat L2)
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
print(f"Training FAISS index with dimension {dim}")
# For IndexFlat, no training needed

# Add vectors to the index
print(f"Adding {embeddings.shape[0]} embeddings to index...")
index.add(embeddings)
print(f"Index size: {index.ntotal} vectors")

# Save the index to disk
index_path = index_dir / f"faiss_index_{embeddings.shape[1]}.index"
faiss.write_index(index, str(index_path))
print(f"FAISS index saved to {index_path}")
