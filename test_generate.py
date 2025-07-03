from backend.app.core.rag_pipeline import retrieve_and_generate

if __name__ == "__main__":
    question = "tu peux me dire les 3 aspects de code de travail en france "
    answer = retrieve_and_generate(question, top_k=5)
    print("Question :", question)
    print("Réponse générée :\n", answer)
