import json

def test_step1(client):
    response = client.get("/api/v1/flow/obskarakter/step1_wawancara")
    assert response.status_code == 200
    assert "present_result_prompt" in response.json()

def test_step2_valid(client):
    scores = [{"kategori": "Aqidah", "score": 80}, {"kategori": "Ibadah", "score": 90}]
    response = client.get(f"/api/v1/flow/obskarakter/step2?scores={json.dumps(scores)}")
    assert response.status_code == 200
    assert "chart_url" in response.json()

def test_step2_invalid_json(client):
    response = client.get("/api/v1/flow/obskarakter/step2?scores=invalid")
    assert response.status_code == 422

def test_step2_invalid_schema(client):
    scores = [{"kategori": "Aqidah", "score": "high"}] # Score should be int
    response = client.get(f"/api/v1/flow/obskarakter/step2?scores={json.dumps(scores)}")
    assert response.status_code == 422
