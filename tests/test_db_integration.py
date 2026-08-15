import json
import pytest
from app.models.domain import Session, Score
from app.database import SessionLocal

def test_db_save_obskarakter(client):
    # Call step 1
    response1 = client.get("/result/v1/flow/obskarakter/step1_wawancara")
    assert response1.status_code == 200
    data1 = response1.json()
    session_id = data1["session_id"]
    
    # Call step 2
    scores = [{"kategori": "Aqidah", "score": 90}]
    response2 = client.get(f"/result/v1/flow/obskarakter/step2?session_id={session_id}&scores={json.dumps(scores)}")
    assert response2.status_code == 200
    
    # Check DB
    db = SessionLocal()
    db_session = db.query(Session).filter(Session.id == session_id).first()
    assert db_session is not None
    
    db_score = db.query(Score).filter(Score.session_id == session_id).first()
    assert db_score is not None
    assert db_score.kategori == "Aqidah"
    assert db_score.score == 90
    db.close()
