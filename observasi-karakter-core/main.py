from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from schemas import AssessmentSubmission
from responses import AssessmentResultPayload
from scoring import calculate_scores
from prefect import flow

app = FastAPI(
    title="Talent Assessment & Personalization Engine API",
    version="1.0.0",
    description="API for processing 40-talent assessments deterministically and serving Web AI payload results.",
)

# Enable CORS so Web AI agents and local micro-frontends can fetch results without blockage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open GET access for web chatbots
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Temporary in-memory store (Replace with Redis or PostgreSQL in production)
DB_STORE: Dict[str, AssessmentResultPayload] = {}

@flow(name="process_assessment_flow")
def process_assessment_flow(payload: AssessmentSubmission) -> AssessmentResultPayload:
    return calculate_scores(payload)

@app.post(
    "/api/v1/assessments",
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="Submit raw user assessment intake",
)
async def submit_assessment(payload: AssessmentSubmission):
    """
    Receives user rankings, personality type, and statement verifications.
    Calculates 40 talent scores deterministically and returns the lookup ID & prompt link.
    """
    result = process_assessment_flow(payload)
    DB_STORE[result.assessment_id] = result

    result_url = f"https://your-domain.com/api/v1/results/{result.assessment_id}"
    
    return {
        "assessment_id": result.assessment_id,
        "result_url": result_url,
        "prompt_template": (
            f"Please fetch my talent assessment JSON payload from {result_url} "
            "and generate my Laporan Lengkap followed by top career choices."
        ),
    }

@app.get(
    "/api/v1/results/{assessment_id}",
    response_model=AssessmentResultPayload,
    status_code=status.HTTP_200_OK,
    summary="Fetch calculated assessment result payload for Web AI",
)
async def get_assessment_result(assessment_id: str):
    """
    Public endpoint fetched by Web AI Chatbots (ChatGPT, Gemini, Claude)
    to retrieve structured JSON metrics.
    """
    if assessment_id not in DB_STORE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment ID not found or expired.",
        )
    return DB_STORE[assessment_id]
