from pydantic import BaseModel, Field, validator
from typing import List, Optional

# --- Common Models ---
class StepResponse(BaseModel):
    session_id: str
    present_result_prompt: str
    next_action: dict
    next_prompt_hint: str
    chart_url: Optional[str] = None

# --- ObsKarakter Models ---
class SubKategoriScore(BaseModel):
    kategori: str = Field(..., description="Nama sub-kategori (misal: 'Termotivasi dalam beribadah')")
    score: int = Field(..., ge=1, le=100, description="Skor evaluasi dari 1 hingga 100")

# --- ObsBakat Models ---
class PersonalData(BaseModel):
    nama_lengkap: str = Field(..., description="Nama lengkap pengguna")
    usia: int = Field(..., gt=0, description="Usia pengguna dalam angka")
    asal_sekolah_institusi: Optional[str] = Field(None, description="Asal sekolah atau institusi")
