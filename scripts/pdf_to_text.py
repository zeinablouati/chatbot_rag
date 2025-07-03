"""
Script pour extraire le texte brut d'un PDF et le découper en chunks.
Déposez le PDF du Code du travail dans `data/raw/code_travail.pdf`.
"""
import os
from pathlib import Path
from pdfminer.high_level import extract_text

# Configuration
data_dir = Path(__file__).parent.parent / "data"
raw_pdf = data_dir / "raw" / "code_travail.pdf"
processed_dir = data_dir / "processed"
chunks_dir = processed_dir / "chunks"
chunk_size = 1000  # nombre de caractères par chunk

# Création des dossiers si nécessaire
processed_dir.mkdir(parents=True, exist_ok=True)
chunks_dir.mkdir(parents=True, exist_ok=True)

# Extraction du texte
print(f"Extraction du texte depuis {raw_pdf}...")
text = extract_text(str(raw_pdf))

# Sauvegarde du texte complet
full_txt = processed_dir / "code_travail_full.txt"
with open(full_txt, "w", encoding="utf-8") as f:
    f.write(text)
print(f"Texte complet sauvegardé dans {full_txt}")

# Découpage en chunks
print(f"Découpage en chunks de {chunk_size} caractères...")
for i in range(0, len(text), chunk_size):
    chunk = text[i : i + chunk_size]
    chunk_file = chunks_dir / f"chunk_{i//chunk_size:04d}.txt"
    with open(chunk_file, "w", encoding="utf-8") as cf:
        cf.write(chunk)
print(f"{len(text)//chunk_size + 1} chunks créés dans {chunks_dir}")
