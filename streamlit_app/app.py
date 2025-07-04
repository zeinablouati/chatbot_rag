import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from backend.app.core.config import settings

# 1) Configuration de la page
st.set_page_config(
    page_title="Chatbot RAG",
    page_icon="🤖",
    layout="wide",
)

# 2) Initialisation de l’historique dans la session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3) Sidebar pour réinitialiser la conversation
with st.sidebar:
    st.title("Options")
    if st.button("🗑 Nouveau chat"):
        st.session_state.chat_history = []
    st.markdown("---")

# 4) Title principal
st.title("🤖 Chatbot RAG")
st.markdown("Posez votre question au Code du travail français et obtenez une réponse concise !")

# 5) Affichage de l’historique sous forme de bulles de chat
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# 6) Zone de saisie interactive (Streamlit >=1.18)
question = st.chat_input("Votre question…")

if question:
    # Affiche immédiatement la bulle utilisateur
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Recherche et génération…"):
        try:
            resp = requests.post(
                f"http://localhost:{settings.api_port}/chat",
                json={"message": question},
                timeout=30
            )
            resp.raise_for_status()
            answer = resp.json().get("response", "")
        except Exception as e:
            answer = f"❌ Erreur lors de l'appel à l'API : {e}"

    # Affiche la réponse
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

# 7) Petit footer
st.markdown("---")
