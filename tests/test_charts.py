import json

def test_chart_obskarakter(client):
    scores = [{"kategori": "Aqidah", "score": 80}, {"kategori": "Ibadah", "score": 90}]
    response = client.get(f"/result/v1/chart/obskarakter?scores={json.dumps(scores)}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0 # make sure there's data

def test_chart_obsbakat(client):
    response = client.get("/result/v1/chart/obsbakat")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0
