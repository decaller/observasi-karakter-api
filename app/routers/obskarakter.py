import json
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession
from pydantic import ValidationError
from app.models.schemas import StepResponse, SubKategoriScore
from app.models.domain import Session, Score
from app.database import get_db

router = APIRouter(prefix="/api/v1/flow/obskarakter", tags=["ObsKarakter"])

MOCKUP_DIR = Path("mockup/obskarakter")

def load_mockup(filename: str) -> dict:
    filepath = MOCKUP_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Mockup file not found"}

@router.get("/step1_wawancara", response_model=StepResponse)
async def obskarakter_step1(db: DBSession = Depends(get_db)):
    """Initializes the Character Growth interview."""
    data = load_mockup("step1_wawancara.json")
    
    # Generate a unique session and save to DB
    new_session_id = f"char_{uuid.uuid4().hex[:8]}"
    db_session = Session(id=new_session_id)
    db.add(db_session)
    db.commit()
    
    data["session_id"] = new_session_id
    
    # Update the prompt hint to tell LLM to pass session_id
    data["next_prompt_hint"] = data.get("next_prompt_hint", "").replace(
        "obskarakter/step2?scores=",
        f"obskarakter/step2?session_id={new_session_id}&scores="
    )
    return data

@router.get("/step2", response_model=StepResponse)
async def obskarakter_step2(
    session_id: str = Query(..., description="The session ID from step 1"),
    scores: str = Query(..., description="JSON array of scores. Example: [{'kategori': 'Aqidah', 'score': 80}]"),
    db: DBSession = Depends(get_db)
):
    """Receives latent scores and returns chart/cross-sell instructions."""
    # Verify session exists
    db_session = db.query(Session).filter(Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session ID not found")

    try:
        parsed_scores = json.loads(scores)
        if not isinstance(parsed_scores, list):
            raise ValueError("Scores must be a JSON array")
        
        # Pydantic strict validation
        validated_scores = [SubKategoriScore(**s) for s in parsed_scores]
        
        # Save validated_scores to the database
        for s in validated_scores:
            new_score = Score(
                session_id=session_id,
                kategori=s.kategori,
                score=s.score,
                tipe_observasi="karakter"
            )
            db.add(new_score)
        db.commit()
        
        data = load_mockup("step2_hasil.json")
        data["session_id"] = session_id
        return data

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format for scores parameter")
    except ValidationError as e:
        # Pydantic validation error will be returned to LLM for self-correction
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

