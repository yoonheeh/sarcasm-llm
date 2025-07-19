from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_evaluate_endpoint():
    """Tests the /api/evaluate endpoint."""
    # Define the request payload
    payload = {"sarcasm_level": "HARD"}

    # Make the POST request
    response = client.post("/api/evaluate", json=payload)

    # Assert that the request was successful
    assert response.status_code == 200

    # Assert that the response is a JSON object
    response_data = response.json()
    assert isinstance(response_data, dict)

    # Assert that the required keys are in the response
    assert "conversation" in response_data
    assert "evaluation_result" in response_data
