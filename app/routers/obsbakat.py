import json
from pathlib import Path
from fastapi import APIRouter
from app.models.schemas import StepResponse

router = APIRouter(prefix="/result/v1/flow/obsbakat", tags=["Obsbakat"])

MOCKUP_DIR = Path("mockup/obsbakat")

def load_mockup(filename: str) -> dict:
    filepath = MOCKUP_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Mockup file not found"}

@router.get("/step1", response_model=StepResponse)
async def obsbakat_step1():
    """Initializes the Talent Mapping interview."""
    data = load_mockup("step1.json")
    return data

@router.get("/step2", response_model=StepResponse)
async def obsbakat_step2():
    """Transitions to deep analysis after capturing personal data."""
    data = load_mockup("step2.json")
    return data

@router.get("/step3", response_model=StepResponse)
async def obsbakat_step3():
    """Iterative funneling of 40 Talent Pillars."""
    data = load_mockup("step3.json")
    return data

@router.get("/step4", response_model=StepResponse)
async def obsbakat_step4():
    """Final curriculum presentation and MVP recommendations."""
    data = load_mockup("step4.json")
    return data
