import sys, os, time
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from backend.app.core.config import settings

st.set_page_config(page_title="Chatbot RAG", page_icon="🤖", layout="wide")

# --- 1) Historique en session ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 2) Sidebar ---
with st.sidebar:
    if st.button("🗑 Nouveau chat"):
        st.session_state.chat_history = []

# --- 3) Zone de chat ---
st.title("🤖 Chatbot RAG")

chat_container = st.container()  # on réaffichera ici tout l'historique

# Affiche l’historique
with chat_container:
    for msg in st.session_state.chat_history:
        ts = msg["timestamp"].strftime("%H:%M:%S")
        if msg["role"] == "user":
            st.chat_message("user", avatar="🙂") \
              .markdown(f"**{msg['content']}**  \n_<sub>{ts}</sub>")
        else:
            st.chat_message("assistant", avatar="🤖") \
              .markdown(f"{msg['content']}  \n_<sub>{ts}</sub>")

# --- 4) Input utilisateur ---
question = st.chat_input("Votre questinnnnnnnnnnnnon…")
if question:
    # 4.1) Ajoute et réaffiche la bulle user
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now()
    })
    # on “reset” le container pour forcer le scroll bas
    chat_container.empty()

    # 4.2) Simulation de “typing…” avant appel API
    typing_msg = st.chat_message("assistant", avatar="🤖")
    spinner = st.empty()
    spinner.markdown("*...tape en cours...*")

    # 4.3) Appel API
    try:
        resp = requests.post(
            f"http://localhost:{settings.api_port}/chat",
            json={"message": question},
            timeout=30
        )
        resp.raise_for_status()
        answer = resp.json().get("response", "")
    except Exception as e:
        answer = f"❌ Erreur : {e}"

    spinner.empty()  # enlève le “typing”

    # 4.4) Effet de dactylographie
    text_holder = st.empty()
    buf = ""
    for ch in answer:
        buf += ch
        text_holder.markdown(buf)
        time.sleep(0.01)  # adapte la vitesse

    # 4.5) Enregistre et réaffiche l’assistant
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer,
        "timestamp": datetime.now()
    })
    # on réaffiche tout pour scroll en bas
    chat_container.empty()

# 5) Footer
st.markdown("---")
st.caption("Prototype RAG • FastAPI + FAISS + Gemini • Streamlit Frontend")
