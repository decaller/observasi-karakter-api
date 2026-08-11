from typing import List, Dict
from pydantic import BaseModel, Field

class TalentScore(BaseModel):
    name: str
    score: int = Field(..., ge=0, le=100)
    category: str

class RecommendedProfession(BaseModel):
    id: str
    title: str
    match_score: str
    required_skills: List[str]

class AssessmentResultPayload(BaseModel):
    assessment_id: str
    created_at: str
    summary: Dict[str, str]
    talent_categories: List[Dict[str, str]]
    calculated_talents: Dict[str, List[TalentScore] | Dict[str, int]]
    recommended_professions: List[RecommendedProfession]
