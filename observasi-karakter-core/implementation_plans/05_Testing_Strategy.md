# 05. Testing Strategy (Pytest & API Tests)

Mengingat aplikasi ini adalah *backend* yang akan terus berinteraksi dengan AI secara dinamis, strategi pengujian (Testing) yang kokoh sangatlah vital. Kita akan menggunakan **Pytest** sebagai framework utama pengujian di FastAPI.

## 1. Unit Testing dengan Pytest
Unit testing berfokus pada fungsi-fungsi isolatif (di luar pemanggilan jaringan/HTTP).
- **Validasi Model Pydantic**: Memastikan bahwa parameter yang salah atau halusinasi dari AI (misal: mengirimkan string ke field integer) benar-benar memicu error validasi Pydantic yang akan membimbing AI melakukan *self-correction*.
- **Pencarian Data (Data Lookup)**: Menguji fungsi-fungsi utilitas yang mengekstrak relasi ID dari `data3.json` atau mencocokkan pilar dengan profesi di `data_profesi.json`.

## 2. API / Integration Testing (FastAPI TestClient)
Pengujian API end-to-end mensimulasikan panggilan dari LLM ke *endpoint* kita menggunakan `fastapi.testclient.TestClient`.
- **Flow Observasi Bakat**:
  - Simulasi `GET /api/v1/flow/obsbakat/step1` hingga `step4` secara berurutan.
  - Memastikan *state* tersimpan dengan benar jika menggunakan database, atau respons *prompt* selanjutnya sudah tepat.
- **Flow Observasi Karakter**:
  - Simulasi pengiriman data laten dari LLM: `GET /api/v1/flow/obskarakter/step2?scores=[...]`.
  - Memastikan endpoint mengembalikan URL *Bar Chart* yang benar dan menginstruksikan transisi (cross-sell) ke *obsbakat*.

## 3. LLM Mocking
Karena kita tidak ingin menghabiskan kuota API (seperti OpenAI/Anthropic) setiap kali menjalankan tes otomatis:
- Kita akan membuat tiruan (Mock) dari LLM yang akan "bertindak" bodoh dan mengirimkan *request* yang salah untuk memastikan sistem merespons dengan HTTP 422 dan pesan error deskriptif.
- Kita akan melakukan *assertion* (penegasan) bahwa setiap JSON yang keluar dari endpoint kita memiliki `present_result_prompt` dan `next_prompt_hint` yang tidak kosong.

## Struktur Folder Test
Nantinya pada *codebase* asli, pengujian akan diletakkan di direktori `tests/`:
```text
tests/
├── conftest.py             # Fixtures untuk FastAPI TestClient dan Mock Data
├── test_obsbakat_flow.py   # API Tests untuk alur 4-langkah bakat
├── test_obskarakter_flow.py# API Tests untuk wawancara karakter & chart
└── test_pydantic_models.py # Unit tests untuk validasi anti-halusinasi AI
```
