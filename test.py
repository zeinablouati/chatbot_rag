from backend.app.core.rag_pipeline import retrieve_top_k

if __name__ == "__main__":
    for txt, dist in retrieve_top_k("Quelles sont les conditions de licenciement ?", k=5):
        print(f"distance {dist:.2f} → {txt[:200]}…\n")
