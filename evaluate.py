#!/usr/bin/env python3
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 1) Chargement des données
DATA = Path(__file__).parent / "data"
PRED_JSON = DATA / "predictions.json"

with open(PRED_JSON, encoding="utf-8") as f:
    samples = json.load(f)

# 2) Modèle d'embeddings
EMB_MODEL = "all-MiniLM-L6-v2"  # ou votre modèle
embedder = SentenceTransformer(EMB_MODEL)

# 3) Préparer les paires prédiction / référence
preds = [s["predicted"] for s in samples]
refs  = [s["reference"] for s in samples]

# 4) Encoder en batch, normalisé pour que dot = cosinus
emb_preds = embedder.encode(preds, normalize_embeddings=True)
emb_refs  = embedder.encode(refs,  normalize_embeddings=True)

# 5) Calcul des cosinus et moyenne
cosines = (emb_preds * emb_refs).sum(axis=1)  # dot product car embeddings normalisés
mean_cosine = float(np.mean(cosines))

# 6) Afficher les résultats
print(f"Nombre de samples : {len(samples)}")
for i, c in enumerate(cosines, 1):
    print(f"  sample {i:02d} — cosinus(pred,ref) = {c:.3f}")
print(f"\n→ Moyenne des cosinus : {mean_cosine:.3f}")

# 7) Code de sortie (utile en CI : échoue si trop bas)
THRESHOLD = 0.75
if mean_cosine < THRESHOLD:
    print(f"❌ Moyenne {mean_cosine:.3f} < seuil {THRESHOLD}")
    exit(1)
else:
    print(f"✅ Moyenne {mean_cosine:.3f} ≥ seuil {THRESHOLD}")
    exit(0)
