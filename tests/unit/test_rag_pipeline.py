import pytest
from backend.app.core.rag_pipeline import retrieve_top_k, summarize_response

@pytest.mark.parametrize("k", [1, 3, 5])
def test_retrieve_top_k_length(k):
    résultats = retrieve_top_k("contrat à durée déterminée", k=k)
    assert isinstance(résultats, list)
    assert len(résultats) == k
    for texte, dist in résultats:
        assert isinstance(texte, str) and texte
        assert isinstance(dist, float)

def test_summarize_response_returns_string():
    detailed = "Ligne1. Ligne2. Ligne3. Ligne4."
    summary = summarize_response(detailed, "Que fait le pipeline ?")
    assert isinstance(summary, str)
    assert summary  
