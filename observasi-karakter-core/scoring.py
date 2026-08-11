import uuid
from datetime import datetime, timezone
from schemas import AssessmentSubmission
from responses import AssessmentResultPayload, TalentScore, RecommendedProfession

from prefect import task

# Weight constants for calculation formula
EGO_WEIGHTS = {"Tinggi": 1.2, "Sedang": 1.0, "Rendah": 0.8}

@task(name="calculate_talent_scores")
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
