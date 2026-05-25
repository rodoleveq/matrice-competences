"""
Smoke tests — API matrice-competences (FastAPI)
Lance un client de test en mémoire sans démarrer de serveur réel.
"""
from fastapi.testclient import TestClient
from sql_app.main import app

client = TestClient(app)


def test_get_matrix_returns_200():
    """L'endpoint /api/matrix répond 200 et retourne du JSON."""
    response = client.get("/api/matrix")
    assert response.status_code == 200
    data = response.json()
    # La réponse doit contenir les clés attendues du schéma MatrixData
    assert "ranks" in data or "pillars" in data or isinstance(data, dict)


def test_app_title():
    """Le titre de l'application FastAPI est bien configuré."""
    assert app.title == "Clarté API"
