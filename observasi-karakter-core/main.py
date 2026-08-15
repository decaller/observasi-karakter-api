import json
import uuid
import os
from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN", "http://127.0.0.1:8000")

# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ── FastAPI App ──────────────────────────────────────────────────────────
app = FastAPI(
    title="Observasi Karakter & Bakat Engine",
    version="2.0.0",
    description="API yang me-render halaman HTML untuk observasi karakter & bakat, dikonsumsi oleh AI web chatbot.",
)

# CORS — tetap terbuka agar AI chatbot bisa mengakses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ── Load Data ────────────────────────────────────────────────────────────
with open(DATA_DIR / "data_karakter.json", "r", encoding="utf-8") as f:
    DATA_KARAKTER = json.load(f)

with open(DATA_DIR / "llms.txt", "r", encoding="utf-8") as f:
    LLMS_TXT = f.read()


# ═════════════════════════════════════════════════════════════════════════
#  ROUTES
# ═════════════════════════════════════════════════════════════════════════

@app.get("/", summary="Homepage — copy prompt untuk AI chatbot")
async def homepage(request: Request):
    """
    Halaman landing yang menampilkan isi llms.txt dengan tombol copy.
    User tinggal tekan tombol copy, lalu paste ke ChatGPT/Claude/Gemini.
    """
    return templates.TemplateResponse(request, "home.html", {
        "llms_txt": LLMS_TXT,
    })


@app.get("/robots.txt", response_class=PlainTextResponse, summary="Robots.txt untuk mengizinkan AI crawler")
async def robots_txt():
    return "User-agent: *\nAllow: /\n"


@app.get(
    "/result/v1/flow/obskarakter/step1_wawancara",
    summary="Step 1 — Daftar indikator wawancara karakter (HTML)",
)
async def step1_wawancara(request: Request):
    """
    Me-render halaman HTML yang berisi:
    - 15 sub-kategori observasi karakter (dari data_karakter.json)
    - Instruksi wawancara (present_result_prompt)
    - Panduan langkah selanjutnya (next_prompt_hint)

    Halaman ini dibaca oleh AI untuk mendapatkan daftar indikator,
    lalu AI memandu wawancara berdasarkan indikator tersebut.
    """
    session_id = f"char_{uuid.uuid4().hex[:8]}"

    present_result_prompt = (
        "Anda adalah Konselor Karakter yang ramah dan interaktif 🛋️. "
        "Di memori Anda telah dimuat dataset 15 Sub-Kategori Pertumbuhan Karakter. "
        "Tujuan Anda adalah mengevaluasi ke-15 sub-kategori ini melalui wawancara cerita yang rileks ☕, "
        "BUKAN dengan memberikan kuesioner kaku."
    )

    next_prompt_hint = (
        "Buka obrolan dengan hangat 👋. Ajukan 1 pertanyaan naratif yang memancing pengguna "
        "untuk bercerita tentang 2 hingga 3 sub-kategori sekaligus secara alami 🌱 "
        "(Contoh: 'Bisa ceritakan bagaimana motivasi sholat putra/putri Anda sehari-hari 🕌, "
        "dan apakah ia sudah terbiasa dengan tata cara wudhu yang benar? 💧'). "
        "Saat pengguna menjawab, secara laten berikan SKOR (1-100) 📝 untuk sub-kategori yang berhasil terjawab. "
        "Lanjutkan wawancara dengan menanyakan kelompok sub-kategori lainnya 🗣️. "
        f"SETELAH WAWANCARA SELESAI (5-7 putaran): Secara opsional, tanyakan kelengkapan data pribadi pengguna 📋. "
        "Setelah data terkumpul, ANDA HARUS BERHENTI BERTANYA 🛑 dan "
        f"PANGGIL URL: {APP_DOMAIN}/result/v1/flow/obskarakter/step2/[array_of_json_scores]. "
        "Contoh format scores: "
        '[{"kategori":"Aqidah","score":80},{"kategori":"Ibadah","score":75},'
        '{"kategori":"Kemandirian","score":40},{"kategori":"Belajar","score":90},'
        '{"kategori":"Bakat","score":85}]. '
        "[PERINGATAN KERAS UNTUK AI]: Anda WAJIB MENGKALKULASI parameter yang dibutuhkan "
        "lalu MERAKIT URL tersebut secara utuh. Setelah itu, COBALAH mengakses URL tersebut. "
        "JIKA BERHASIL, lanjutkan instruksi sesuai respons halaman. "
        "JIKA GAGAL, berikan TAUTAN URL lengkap tersebut kepada pengguna agar mereka bisa mengkliknya sendiri."
    )

    return templates.TemplateResponse(request, "step1_wawancara.html", {
        "data_karakter": DATA_KARAKTER,
        "session_id": session_id,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })


@app.get(
    "/result/v1/flow/obskarakter/step2/{scores:path}",
    summary="Step 2 — Laporan hasil observasi karakter (HTML)",
)
async def step2_hasil(request: Request, scores: str):
    """
    Me-render halaman HTML berisi laporan hasil observasi:
    - Skor per kategori (bar chart visual)
    - Instruksi AI untuk analisis empatik
    - Cross-sell ke Observasi Bakat

    Parameter `scores` adalah JSON array yang di-encode di path URL.
    Contoh: /step2/[{"kategori":"Aqidah","score":80},{"kategori":"Ibadah","score":75}]
    """
    session_id = f"char_{uuid.uuid4().hex[:8]}"

    # Decode & parse scores from path
    decoded_scores = unquote(scores)
    try:
        parsed_scores = json.loads(decoded_scores)
    except json.JSONDecodeError:
        parsed_scores = []

    # Build chart URL (QuickChart.io)
    labels = [s.get("kategori", "?") for s in parsed_scores]
    values = [s.get("score", 0) for s in parsed_scores]
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Skor Realita",
                "data": values,
                "backgroundColor": [
                    "rgba(52, 211, 153, 0.7)" if v >= 75
                    else "rgba(251, 191, 36, 0.7)" if v >= 50
                    else "rgba(248, 113, 113, 0.7)"
                    for v in values
                ],
            }],
        },
        "options": {
            "scales": {"y": {"beginAtZero": True, "max": 100}},
            "plugins": {"title": {"display": True, "text": "Skor Pertumbuhan Karakter"}},
        },
    }
    from urllib.parse import quote
    chart_url = f"https://quickchart.io/chart?c={quote(json.dumps(chart_config))}"

    present_result_prompt = (
        "✅ Anda telah menerima konfirmasi dari server bahwa data skor telah tersimpan. "
        "Sekarang saatnya menyajikan Laporan Hasil Observasi Karakter kepada pengguna 📈. "
        "1. Tampilkan grafik perbandingan skor yang sudah tersedia di halaman ini 📊. "
        "2. Berikan analisis empatik ❤️ tentang jarak antara 'Skor Realita' dan 'Ekspektasi Umur'. "
        "Beritahu area mana saja yang sudah sangat baik 🌟, dan area mana yang menjadi PR utama "
        "sebelum anak baligh 🎯. "
        "3. Berikan saran-saran praktis pengasuhan (parenting) 👨‍👩‍👧‍👦 untuk menutupi celah kelemahan tersebut."
    )

    next_prompt_hint = (
        "Setelah menyajikan analisis grafik secara komprehensif, tawarkan pengguna untuk beralih "
        "ke Pemetaan Bakat 🗺️ dengan mengatakan: 'Kita sudah memiliki peta dasar pertumbuhan karakter 🌱. "
        "Langkah selanjutnya yang sangat krusial adalah memetakan potensi bawaan (bakat) dan arah "
        "karirnya di masa depan 🚀. Apakah Anda ingin melanjutkan ke fase Observasi Bakat (40 Pilar) sekarang? 🤔' "
        "Jika pengguna setuju, langsung PANGGIL URL: "
        f"{APP_DOMAIN}/result/v1/flow/obsbakat/step1 🔗. "
        "[PERINGATAN KERAS UNTUK AI]: Anda WAJIB merakit URL secara utuh. "
        "JIKA GAGAL mengakses, berikan TAUTAN URL lengkap kepada pengguna."
    )

    return templates.TemplateResponse(request, "step2_hasil.html", {
        "scores": parsed_scores,
        "session_id": session_id,
        "chart_url": chart_url,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })


# ═════════════════════════════════════════════════════════════════════════
#  OBSERVASI BAKAT (OBSBAKAT) ROUTES
# ═════════════════════════════════════════════════════════════════════════

@app.get(
    "/result/v1/flow/obsbakat/step1",
    summary="Step 1 — Pemetaan Awal Bakat (HTML)",
)
async def obsbakat_step1(request: Request, p: str = "50", ego: str = "t,s,r"):
    session_id = f"bkt_{uuid.uuid4().hex[:8]}"

    present_result_prompt = (
        "👋 Halo! Anda adalah Asisten Eksplorasi Minat yang hangat dan interaktif. "
        "Anda sedang berbicara dengan pengguna yang belum pernah dievaluasi."
    )

    next_prompt_hint = (
        "Sapa pengguna dengan antusias (gunakan emoji ramah seperti 👋 atau ✨). "
        "Ajukan SATU atau DUA pertanyaan ringan tentang hobi, apa yang sering mereka lakukan di waktu luang, "
        "atau aktivitas apa yang membuat mereka lupa waktu. Jangan menginterogasi, biarkan mengalir seperti obrolan santai di kafe ☕. "
        "Setelah pengguna menjawab atau menceritakan hobinya, ANDA HARUS BERHENTI BERTANYA dan "
        f"segera panggil tautan berikut: {APP_DOMAIN}/result/v1/flow/obsbakat/step2 "
        "untuk melanjutkan ke tahap pengumpulan data personal."
    )

    return templates.TemplateResponse(request, "obsbakat_step1.html", {
        "session_id": session_id,
        "p": p,
        "ego": ego,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })


@app.get(
    "/result/v1/flow/obsbakat/step2",
    summary="Step 2 — Data Personal Bakat (HTML)",
)
async def obsbakat_step2(request: Request):
    session_id = f"bkt_{uuid.uuid4().hex[:8]}"

    present_result_prompt = (
        "🎉 Hebat! Anda telah memicu rasa ingin tahu pengguna."
    )

    next_prompt_hint = (
        "Berikan apresiasi singkat (misalnya 'Wah, menarik sekali! 🤩'). Sebelum kita masuk ke analisis mendalam, "
        "tanyakan kelengkapan data pribadi pengguna (Nama Lengkap, Usia, dan Organisasi/Event jika ada) secara ramah 📋. "
        "JANGAN berikan kesimpulan akhir atau memanggil API sebelum data ini terkumpul. "
        "Setelah semua data diri tersebut terkumpul dari pengguna, Segera panggil tautan berikut: "
        f"{APP_DOMAIN}/result/v1/flow/obsbakat/step3"
    )

    return templates.TemplateResponse(request, "obsbakat_step2.html", {
        "session_id": session_id,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })


@app.get(
    "/result/v1/flow/obsbakat/step3",
    summary="Step 3 — Analisis 40 Pilar Bakat (HTML)",
)
async def obsbakat_step3(request: Request):
    session_id = f"bkt_{uuid.uuid4().hex[:8]}"

    # Load data3.json and data_profesi.json
    try:
        with open(DATA_DIR / "data3.json", "r", encoding="utf-8") as f:
            data3 = json.load(f)
    except FileNotFoundError:
        data3 = {"error": "data3.json not found"}

    try:
        with open(DATA_DIR / "data_profesi.json", "r", encoding="utf-8") as f:
            data_profesi = json.load(f)
    except FileNotFoundError:
        data_profesi = {"error": "data_profesi.json not found"}

    present_result_prompt = (
        "📊 Keren! Anda kini memiliki data awal dan data pribadi pengguna."
    )

    next_prompt_hint = (
        "Gali lebih dalam! 🕵️‍♂️ Ajukan pertanyaan lanjutan yang lebih tajam berdasarkan jawaban mereka "
        "sebelumnya untuk membedakan antara sekadar hobi atau potensi sejati. Gunakan teknik funneling (mengerucut) 🎯. "
        "Setelah Anda selesai melakukan funneling dan minat pengguna sudah cukup mengerucut, Segera panggil tautan berikut: "
        f"{APP_DOMAIN}/result/v1/flow/obsbakat/step4?data=analisis_selesai "
        "untuk memberikan rekomendasi final."
    )

    return templates.TemplateResponse(request, "obsbakat_step3.html", {
        "session_id": session_id,
        "data3": data3,
        "data_profesi": data_profesi,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })


@app.get(
    "/result/v1/flow/obsbakat/step4",
    summary="Step 4 — Hasil Akhir Bakat (HTML)",
)
async def obsbakat_step4(request: Request, data: str = ""):
    session_id = f"bkt_{uuid.uuid4().hex[:8]}"

    # Try to decode if there's any data passed in URL
    parsed_data = {"status": "Analisis selesai"}
    if data:
        try:
            parsed_data = json.loads(unquote(data))
        except:
            parsed_data = {"raw_data": data}

    present_result_prompt = (
        "🏆 Luar biasa! Wawancara telah selesai. Sekarang Anda harus mempresentasikan kesimpulan "
        "bakat pengguna berdasarkan kerangka 40 pilar dan data profesi."
    )

    next_prompt_hint = (
        "Sajikan Curriculum Personal yang mencakup kekuatan utama, kelemahan, dan rekomendasi aktivitas "
        "(MVP - Minimum Viable Product) secara bertingkat. Berikan dorongan semangat sebagai penutup!"
    )

    return templates.TemplateResponse(request, "obsbakat_step4.html", {
        "session_id": session_id,
        "result_data": parsed_data,
        "present_result_prompt": present_result_prompt,
        "next_prompt_hint": next_prompt_hint,
    })
