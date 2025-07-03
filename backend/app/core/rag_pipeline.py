"""
Module de pipeline RAG :
- Retrieval via FAISS + SentenceTransformers
- Construction du prompt avec les passages récupérés
- Génération via Google Gemini API
"""
import os
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from google import genai
from typing import List, Tuple
from backend.app.core.config import settings



# Configuration des chemins
project_root = Path(__file__).resolve().parents[3]
data_dir = project_root / "data"
chunks_dir = data_dir / "processed" / "articles"
vectorstore_dir = data_dir / "vectorstore"

# Chargement des chunks de texte
chunk_paths = sorted(chunks_dir.glob("*.txt"))
chunk_texts = [p.read_text(encoding="utf-8") for p in chunk_paths]

# Chargement de l'index FAISS
index_files = list(vectorstore_dir.glob("faiss_index_*.index"))
if not index_files:
    raise FileNotFoundError(f"Pas d'index FAISS trouvé dans {vectorstore_dir}")
index = faiss.read_index(str(index_files[0]))

# Modèle d'embeddings
emb_model_name = os.getenv("EMBEDDING_MODEL", settings.embedding_model)
embedder = SentenceTransformer(emb_model_name)

# Configuration Gemini
gemini_api_key = settings.gemini_api_key
gemini_model_name = settings.gemini_model_name
client = genai.Client(api_key=gemini_api_key)


def retrieve_top_k(question: str, k: int = 5):
    """
    Retourne les k passages les plus proches de la question.
    """
    # Encode la question
    q_emb = embedder.encode(question)
    q_emb = np.array([q_emb], dtype="float32")
    # Recherche dans FAISS
    distances, indices = index.search(q_emb, k)
    # Construction de la liste (texte, distance)
    return [(chunk_texts[idx], float(dist)) for dist, idx in zip(distances[0], indices[0])]

def build_rag_prompt(question: str, passages: list[tuple[str, float]]) -> str:
    """
    Construit un prompt RAG à partir de la question et des passages récupérés.
    """
    # 1) Instructions système
    prompt = (
        "Vous êtes un assistant expert en droit du travail. "
        "Utilisez les extraits ci-dessous pour répondre précisément à la question.\n\n"
    )
    # 2) Ajout des passages
    for i, (text, dist) in enumerate(passages, start=1):
        prompt += f"--- Passage {i} (distance {dist:.2f}) ---\n"
        prompt += text.strip() + "\n\n"
    # 3) Question finale
    prompt += f"Question : {question}\nRéponse :"
    return prompt

def retrieve_and_generate(question: str, top_k: int = 5, concise: bool = False) -> str:
    # 1) retrieval
    passages = retrieve_top_k(question, k=top_k)
    # 2) construction du prompt RAG
    prompt = build_rag_prompt(question, passages)
    # 3) génération détaillée
    response = client.models.generate_content(
        model=settings.gemini_model_name,
        contents=[{"parts":[{"text": prompt}]}]
    ).text

    # 4) si on veut une version concise, on passe par le résumé
    if concise:
        return summarize_response(response, question)

    # 5) sinon on renvoie la réponse détaillée
    return response


def summarize_response(detailed_answer: str, question: str) -> str:
    """
    Prend la réponse détaillée (avec extraits) et renvoie
    une version concise, en un paragraphe ou une phrase.
    """
    # Construire un prompt de résumé
    prompt_text = (
        "Vous êtes un assistant expert en droit du travail. "
        "À partir de la réponse suivante, fournissez une version "
        "très concise (1 paragraphe ou 1 phrase) qui réponde directement à la question.\n\n"
        f"Question : {question}\n\n"
        f"Réponse détaillée :\n{detailed_answer}\n\n"
        "Réponse concise :"
    )

    # Appel à Gemini pour le résumé
    response = client.models.generate_content(
        model=settings.gemini_model_name,
        contents=[{"parts":[{"text": prompt_text}]}]
    )
    return response.text.strip()
