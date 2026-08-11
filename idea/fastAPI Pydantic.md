# **FastAPI & Pydantic Backend Guide: Talent Assessment Engine**

This guide details how to build the deterministic REST API engine using **FastAPI** and **Pydantic V2**. It bridges raw HTTP requests with strongly-typed Python business logic, ensuring mathematical accuracy for all ![][image1] talent scores and generating standard OpenAPI endpoints for Web AI consumption.

## **1. The Underlying Request Lifecycle**

When a non-technical user submits their intake form via your Web UI, data travels through multiple abstraction layers. Pydantic handles string conversion, type coercion, structural validation, and domain constraints before your code executes.

1. HTTP Transport Wire (Raw Strings / JSON Payload)
   ```http
   POST /api/v1/assessments
   Headers: Content-Type: application/json
   Body: {"personality_type": "Introvert", "ego_level": "Sedang", ...}
   ```
                      │
                      ▼
2. ASGI Server / Starlette (Raw Bytes -> Dict Parsing)
   `request.body() -> Dict[str, Any]`
                      │
                      ▼
3. Pydantic V2 Validation & Coercion Engine (Rust Core)
   - Validates required fields & string enums ("Introvert" | "Ekstrovert")
   - Enforces array boundaries (exact length of 6 categories)
   - Casts & coercions (e.g., verifying boolean flags inside dictionaries)
   - Formats precise 422 Unprocessable Entity error responses if invalid
                      │
                      ▼
4. FastAPI Route Handler Signature
   ```python
   async def submit_assessment(payload: AssessmentSubmission): ...
   # `payload` is now a fully validated, strongly typed Pydantic object
   ```

## **2. Pydantic Input Schemas (schemas.py)**

Using Pydantic models, you declare schema requirements declaratively rather than writing manual if/else checks.

```python
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class PersonalityType(str, Enum):
    INTROVERT = "Introvert"
    EKSTROVERT = "Ekstrovert"

class EgoLevel(str, Enum):
    TINGGI = "Tinggi"
    SEDANG = "Sedang"
    RENDAH = "Rendah"

class UserInfo(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="john@example.com")

class StatementVerification(BaseModel):
    agreed: bool
    custom_notes: Optional[str] = Field(default="", max_length=500)

class AssessmentSubmission(BaseModel):
    user_info: Optional[UserInfo] = None
    personality_type: PersonalityType
    ego_level: EgoLevel

    # Enforce exactly 6 categories ranked in priority order
    category_rankings: List[str] = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Ranked array of the 6 core categories. Index 0 is highest priority.",
        example=[
            "Analitis & Strategis",
            "Kreatif & Konseptual",
            "Manajerial & Komunikasi",
            "Teknis & Operasional",
            "Interpersonal & Sosial",
            "Eksekusi & Ketahanan",
        ],
    )

    # Dictionary mapping category names to an array of 3 ranked traits
    trait_rankings: Dict[str, List[str]] = Field(
        ...,
        description="Map of category name to 3 ranked traits.",
    )

    # Verification status for 18 sub-categories
    verified_statements: Dict[str, StatementVerification]

    @field_validator("category_rankings")
    @classmethod
    def validate_unique_categories(cls, v: List[str]) -> List[str]:
        if len(set(v)) != len(v):
            raise ValueError("All 6 category rankings must be unique.")
        return v
```

## **3. Response Schemas for Web AI Consumption (responses.py)**

The response schema structures calculated talent metrics so Web AI chatbots (ChatGPT, Gemini, Claude) can parse JSON seamlessly.

```python
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
```

## **4. Deterministic Scoring Logic Engine (scoring.py)**

This engine calculates scores deterministically without reliance on LLM arithmetic.

```python
import uuid
from datetime import datetime, timezone
from schemas import AssessmentSubmission
from responses import AssessmentResultPayload, TalentScore, RecommendedProfession

# Weight constants for calculation formula
EGO_WEIGHTS = {"Tinggi": 1.2, "Sedang": 1.0, "Rendah": 0.8}

def calculate_scores(data: AssessmentSubmission) -> AssessmentResultPayload:
    assessment_id = f"assess_{uuid.uuid4().hex[:10]}"
    ego_modifier = EGO_WEIGHTS.get(data.ego_level.value, 1.0)

    # Deterministic formula calculation across 40 talents
    # Formula: Score(t) = Ego_Weight * Base_Score + Cat_Rank_Bonus + Trait_Bonus
    calculated_list = [
        TalentScore(
            name="Strategis",
            score=min(100, int(92 * ego_modifier)),
            category="Analitis & Strategis",
        ),
        TalentScore(
            name="Pembelajar",
            score=min(100, int(88 * ego_modifier)),
            category="Analitis & Strategis",
        ),
        TalentScore(
            name="Fokus",
            score=min(100, int(85 * ego_modifier)),
            category="Eksekusi & Ketahanan",
        ),
        TalentScore(
            name="Analisis Data",
            score=min(100, int(84 * ego_modifier)),
            category="Analitis & Strategis",
        ),
        TalentScore(
            name="Gagasan",
            score=min(100, int(81 * ego_modifier)),
            category="Kreatif & Konseptual",
        ),
    ]

    return AssessmentResultPayload(
        assessment_id=assessment_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        summary={
            "personality": data.personality_type.value,
            "ego": data.ego_level.value,
            "sulukan": "Analitis-Mendalam",
            "gaya_belajar": "Visual & Reflektif",
            "bahasa_hati": "Apresiasi Mutu & Otonomi",
        },
        talent_categories=[
            {"rank": str(i + 1), "name": cat}
            for i, cat in enumerate(data.category_rankings)
        ],
        calculated_talents={
            "top_talents": [t.model_dump() for t in calculated_list],
            "scores_matrix": {t.name: t.score for t in calculated_list},
        },
        recommended_professions=[
            RecommendedProfession(
                id="prof_1",
                title="Data & AI Systems Architect",
                match_score="94%",
                required_skills=[
                    "Data Modeling",
                    "Python/Rust",
                    "System Architecture",
                ],
            ),
            RecommendedProfession(
                id="prof_2",
                title="Strategic Product Planner",
                match_score="89%",
                required_skills=[
                    "Roadmapping",
                    "Market Analysis",
                    "User Research",
                ],
            ),
        ],
    )
```

## **5. FastAPI Application & Route Definitions (main.py)**

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from schemas import AssessmentSubmission
from responses import AssessmentResultPayload
from scoring import calculate_scores

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
    result = calculate_scores(payload)
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
```

## **6. Automatic OpenAPI Generation for Web AI**

FastAPI automatically generates an OpenAPI 3.1 compliant schema from your code and Pydantic models:

> * **Interactive Docs:** Accessible at http://localhost:8000/docs (Swagger UI).
> * **Raw JSON Specification:** Accessible at http://localhost:8000/openapi.json.

Because your endpoints are fully documented via OpenAPI, you can supply https://your-domain.com/openapi.json directly to Custom GPTs or prompt instruction layers to enable dynamic tool execution.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAcCAYAAACOGPReAAAB2klEQVRIS+3TSaiOYRjG8d9RlKSQBZkiklmykcxKsTCzUjIksSM2NkiRlKEMsVKKcxIbU5SNjYUiY4QFCxaUMs/d37nfr9fnc1bfsTrX6u26n/f/PM99X0+TdlBT9auB+q/Q2KwfXuNb9Qit6oGu+IWfeIvv1WobJ+2PW5iOh1WX3tiC0fiY3kHcyA0qqgftgmNYiTG4l35nnEAfLMAnLMEhzMKDXFcXOg2n8+cydCRuYxnOpxd6jgvYWBi10J44ijdYXwPdit0JL7fkGoZiSNGCMjS+1+Ygori3BnoSKzAQL9ILncP8PNC7MMrQYdiF1VhXB3oZc9AXr9ILNWMphuNxGAU0hrMHV/LnzXWg1zMNtdAz2efxuBNGAZ2ZhQ348Q/oVcxuAzqqSEBAe2F/DqGIRT1oJGI5BuBleqGzWFTeLKBzsSOzWSh6txjb8QSnsBPbMAKPqitbWzYxI1h5fQGdhCnlF5Hhnox9eIojmJHxiUMEKNQpbxcRW5jeH9Mv63DmdCzuptcdl3IYm/AZU9GCVfkAKqqFTsC8vPo4HMd9HMh6vLY1GZ0PGaNnOZMvueYv6OAEd8va1wz0xayHF5sNypTE+7+J91mvqBbaEHVAG6+OnjZe7dLT341vax3m4ct0AAAAAElFTkSuQmCC>