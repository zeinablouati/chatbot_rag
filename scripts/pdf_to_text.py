"""
Script pour extraire le texte brut d'un PDF et le découper par articles L du Code du travail.
Déposez le PDF du Code du travail dans `data/raw/code_travail.pdf`.
"""
import re
from pathlib import Path
from pdfminer.high_level import extract_text

# Configuration
data_dir     = Path(__file__).parent.parent / "data"
raw_pdf      = data_dir / "raw" / "code_travail.pdf"
processed_dir= data_dir / "processed"
articles_dir = processed_dir / "articles"

# Création des dossiers si nécessaire
processed_dir.mkdir(parents=True, exist_ok=True)
articles_dir.mkdir(parents=True, exist_ok=True)

# Extraction du texte
print(f"Extraction du texte depuis {raw_pdf}…")
text = extract_text(str(raw_pdf))

# Sauvegarde du texte complet
full_txt = processed_dir / "code_travail_full.txt"
with open(full_txt, "w", encoding="utf-8") as f:
    f.write(text)
print(f"Texte complet sauvegardé dans {full_txt}")

# Découpage par articles (Article Lxxx)
print("Découpage selon les articles L...")
pattern = re.compile(r"(Article\s+L[\d\-]+)", re.UNICODE)
matches = list(pattern.finditer(text))

articles = []
for i, match in enumerate(matches):
    title = match.group(1).strip()
    start = match.end()
    # la fin du contenu est le début du prochain match, ou la fin du texte
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    content = text[start:end].strip()
    articles.append({"name": title, "content": content})

print(f"{len(articles)} articles détectés, sauvegarde dans {articles_dir}…")

# Enregistrement de chaque article dans un fichier
for art in articles:
    # création d'un nom de fichier sûr (sans espaces ni caractères interdits)
    safe_name = art["name"].replace(" ", "_").replace(":", "").replace("/", "_")
    article_file = articles_dir / f"{safe_name}.txt"
    with open(article_file, "w", encoding="utf-8") as af:
        af.write(art["content"])

print(f"{len(articles)} fichiers d’articles créés dans {articles_dir}")
