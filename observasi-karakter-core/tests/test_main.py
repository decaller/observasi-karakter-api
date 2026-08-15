from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_homepage_returns_html():
    """Homepage harus me-render HTML dengan konten llms.txt dan tombol copy."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    # Pastikan elemen kunci ada
    assert "Observasi Karakter" in resp.text
    assert "Copy ke Clipboard" in resp.text
    assert "llms-content" in resp.text  # id dari pre element


def test_homepage_contains_llms_txt():
    """Homepage harus memuat isi llms.txt di dalam halaman."""
    resp = client.get("/")
    # Cek beberapa string kunci dari llms.txt
    assert "Peran Anda" in resp.text
    assert "OBSERVASI_KARAKTER" in resp.text


def test_step1_wawancara_returns_html():
    """Step 1 wawancara harus me-render HTML dengan 15 sub-kategori."""
    resp = client.get("/result/v1/flow/obskarakter/step1_wawancara")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    # Cek beberapa sub-kategori dari data_karakter.json muncul
    assert "Termotivasi dalam beribadah" in resp.text
    assert "Merasa diawasi oleh Allah" in resp.text
    assert "Mampu bersosial" in resp.text
    assert "Tekun dan kreatif memecahkan masalah" in resp.text


def test_step1_contains_session_id():
    """Step 1 harus mengandung session_id."""
    resp = client.get("/result/v1/flow/obskarakter/step1_wawancara")
    assert "char_" in resp.text


def test_step1_contains_instruction_blocks():
    """Step 1 harus mengandung instruksi untuk AI."""
    resp = client.get("/result/v1/flow/obskarakter/step1_wawancara")
    assert "Konselor Karakter" in resp.text
    assert "SETELAH WAWANCARA SELESAI" in resp.text


def test_step2_hasil_returns_html():
    """Step 2 hasil harus me-render HTML dengan skor."""
    scores = '[{"kategori":"Aqidah","score":80},{"kategori":"Ibadah","score":75}]'
    resp = client.get(f"/result/v1/flow/obskarakter/step2/{scores}")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Aqidah" in resp.text
    assert "80" in resp.text
    assert "Ibadah" in resp.text
    assert "75" in resp.text


def test_step2_renders_score_cards():
    """Step 2 harus me-render score cards dengan warna yang benar."""
    scores = '[{"kategori":"Aqidah","score":90},{"kategori":"Kemandirian","score":40}]'
    resp = client.get(f"/result/v1/flow/obskarakter/step2/{scores}")
    # Score 90 -> class "high", score 40 -> class "low"
    assert "high" in resp.text
    assert "low" in resp.text


def test_step2_contains_chart_url():
    """Step 2 harus mengandung chart URL dari QuickChart."""
    scores = '[{"kategori":"Aqidah","score":80}]'
    resp = client.get(f"/result/v1/flow/obskarakter/step2/{scores}")
    assert "quickchart.io" in resp.text


def test_step2_contains_cross_sell():
    """Step 2 harus mengandung link cross-sell ke observasi bakat."""
    scores = '[{"kategori":"Aqidah","score":80}]'
    resp = client.get(f"/result/v1/flow/obskarakter/step2/{scores}")
    assert "Observasi Bakat" in resp.text
    assert "/result/v1/flow/obsbakat/step1" in resp.text


def test_step2_invalid_scores_graceful():
    """Step 2 harus tetap render meskipun scores tidak valid JSON."""
    resp = client.get("/result/v1/flow/obskarakter/step2/invalid_json")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
