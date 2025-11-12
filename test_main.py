from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_evaluate_endpoint():
    """Tests the /api/evaluate endpoint."""
    # Define the request parameters
    params = {"sarcasm_level": "HARD", "model_to_evaluate": "gemini"}

    # Make the GET request
    response = client.get("/api/evaluate", params=params)

    # Assert that the request was successful
    assert response.status_code == 200
