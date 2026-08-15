def test_step1(client):
    response = client.get("/result/v1/flow/obsbakat/step1")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "present_result_prompt" in data
    assert "next_action" in data

def test_step2(client):
    response = client.get("/result/v1/flow/obsbakat/step2")
    assert response.status_code == 200
    assert "next_prompt_hint" in response.json()

def test_step3(client):
    response = client.get("/result/v1/flow/obsbakat/step3")
    assert response.status_code == 200
    assert "next_prompt_hint" in response.json()

def test_step4(client):
    response = client.get("/result/v1/flow/obsbakat/step4")
    assert response.status_code == 200
    assert "present_result_prompt" in response.json()
