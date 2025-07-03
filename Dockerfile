# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app

# 1) Copier liste des dépendances et installer TOUT (API + UI)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn[standard] streamlit requests pydantic-settings

# 2) Copier le code
COPY backend       ./backend
COPY data          ./data
COPY streamlit_app ./streamlit_app

# 3) Configurer et exposer les ports
ENV API_PORT=8000
EXPOSE 8000 8501

# Copier le .env pour que Pydantic-Settings le lise
COPY .env .env


# 4) Lancer API et UI en parallèle
CMD ["bash", "-lc", "\
    uvicorn backend.app.main:app --host 0.0.0.0 --port $API_PORT & \
    streamlit run streamlit_app/app.py --server.port 8501 --server.headless true\
"]
