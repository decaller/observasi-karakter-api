# 03. Observasi Karakter API Specification

Track ini dirancang untuk mengevaluasi 45 Indikator Pertumbuhan Karakter Anak (Iman, Aqidah, Ibadah, Kemandirian, Belajar, Bakat) dan menghubungkannya dengan tingkat kesiapan *Baligh*.

## 1. `GET /result/v1/flow/obskarakter/step1_wawancara`
**Purpose:** Menginisiasi wawancara observasi karakter berbasis pengelompokan 15 sub-kategori.

- **Backend Action:**
  - Memberitahu AI bahwa ia adalah Konselor Karakter.
  - Menginstruksikan AI untuk menggabungkan pertanyaan yang meng-cover 2-3 sub-kategori sekaligus agar efisien.
  - Menginstruksikan AI untuk mencatat skor (1-100) secara *laten* (di belakang layar).
  - Saat wawancara dirasa cukup (setelah 5-7 putaran) dan data pribadi opsional telah terkumpul, AI dipandu untuk berhenti dan mensubmit datanya via `/step2`.

---

## 2. `GET /result/v1/flow/obskarakter/step2`
**Purpose:** Menerima data skor dari AI, memproses, dan menyajikan laporan akhir serta menjembatani ke produk berikutnya (Cross-Selling).

- **Query Parameters (Pydantic Model):**
  - `scores` (list of dict): Menyimpan array skor 15 sub-kategori yang telah dihimpun AI.
  
- **Backend Action:**
  - Menyimpan `scores` ke database relasional (PostgreSQL/MongoDB) yang ditenagai FastAPI untuk *historical tracking* pengguna.
  - Mengembalikan *prompt* yang berisi *Bar Chart URL* (misal via QuickChart.io) untuk membandingkan **Skor Realita** dengan **Ekspektasi Umur**.
  - Menginstruksikan AI untuk memberikan nasehat *Parenting* tentang apa yang harus dipacu sebelum usia Baligh.
  - **Cross-Sell Trigger:** Menginstruksikan AI di akhir laporannya untuk menawarkan kelanjutan layanan: "Apakah Anda ingin melanjutkan ke pemetaan Observasi Bakat (40 Pilar)?", yang akan otomatis mengarahkan panggilan ke `/result/v1/flow/obsbakat/step1`.
