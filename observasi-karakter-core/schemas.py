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
    name: Optional[str] = Field(None, examples=["John Doe"])
    email: Optional[EmailStr] = Field(None, examples=["john@example.com"])

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
        examples=[
            [
                "Analitis & Strategis",
                "Kreatif & Konseptual",
                "Manajerial & Komunikasi",
                "Teknis & Operasional",
                "Interpersonal & Sosial",
                "Eksekusi & Ketahanan",
            ]
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
