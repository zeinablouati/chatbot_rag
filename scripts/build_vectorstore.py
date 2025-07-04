import os
import numpy as np
import faiss
from pathlib import Path

BASE_DIR        = Path(__file__).resolve().parents[1]
DATA_DIR        = BASE_DIR / "data"
EMBEDDINGS_DIR  = DATA_DIR / "embeddings"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"

# 1) Crée le dossier vectorstore s'il n'existe pas
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# 2) Recherche du fichier d'embeddings
emb_files = list(EMBEDDINGS_DIR.glob("embeddings_*.npz"))
if not emb_files:
    raise FileNotFoundError(f"No embeddings file found in {EMBEDDINGS_DIR}")
emb_path = emb_files[0]
print(f"Loading embeddings from {emb_path}")

# 3) Chargement des embeddings
data = np.load(emb_path)
embeddings = data["embeddings"].astype("float32")

# 4) Construction de l'index FAISS
dim   = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
print(f"Training FAISS index with dimension {dim}")
index.add(embeddings)
print(f"Index size: {index.ntotal} vectors")

# 5) Sauvegarde de l'index
index_path = VECTORSTORE_DIR / f"faiss_index_{dim}.index"
faiss.write_index(index, str(index_path))
print(f"FAISS index saved to {index_path}")
