import pytest
from pydantic import ValidationError
from app.models.schemas import SubKategoriScore, PersonalData

def test_subkategori_score_valid():
    model = SubKategoriScore(kategori="Aqidah", score=85)
    assert model.kategori == "Aqidah"
    assert model.score == 85

def test_subkategori_score_invalid_range():
    with pytest.raises(ValidationError):
        SubKategoriScore(kategori="Aqidah", score=150)
    with pytest.raises(ValidationError):
        SubKategoriScore(kategori="Aqidah", score=0)

def test_personal_data_valid():
    model = PersonalData(nama_lengkap="Budi", usia=12, asal_sekolah_institusi="SDN 1")
    assert model.nama_lengkap == "Budi"
    assert model.usia == 12

def test_personal_data_invalid():
    with pytest.raises(ValidationError):
        PersonalData(nama_lengkap="Budi", usia="dua belas") # Should be int
