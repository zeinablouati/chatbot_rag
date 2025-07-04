"""
Script pour calculer les embeddings des chunks de texte et les sauvegarder.
"""
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# Configuration
data_dir = Path(__file__).parent.parent / "data"
chunks_dir = data_dir / "processed" / "chunks"
embeddings_dir = data_dir / "embeddings"
model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Création du dossier d'embeddings si nécessaire
embeddings_dir.mkdir(parents=True, exist_ok=True)

# Chargement du modèle
print(f"Chargement du modèle d'embeddings: {model_name}...")
model = SentenceTransformer(model_name)

# Lecture des chunks et calcul des embeddings
files = sorted(chunks_dir.glob("*.txt"))
print(f"{len(files)} chunks trouvés. Calcul des embeddings...")
embeddings = []
for file in files:
    text = file.read_text(encoding="utf-8")
    emb = model.encode(text)
    embeddings.append(emb)

embeddings = np.vstack(embeddings)

# Sauvegarde
embeddings_path = embeddings_dir / f"embeddings_{model_name}.npz"
np.savez_compressed(embeddings_path, embeddings=embeddings)
print(f"Embeddings sauvegardés dans {embeddings_path}")
