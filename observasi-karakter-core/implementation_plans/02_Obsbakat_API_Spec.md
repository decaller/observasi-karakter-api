# 02. Observasi Bakat (40 Pilar) API Specification

Track ini dirancang untuk memandu pengguna dalam mengeksplorasi potensi dan bakat bawaan (berbasis 40 Pilar). Proses ini dibagi menjadi 4 Step berurutan yang saling menyuapkan data ke LLM.

## Backend Implementation Note (FastAPI)
- Semua *endpoint* harus menggunakan `method: GET` karena LLM akan memanggilnya sebagai `tools/functions` dalam *chat context* yang biasanya menggunakan standard HTTP GET.
- *Responses* (kembalian API) harus berformat JSON yang mendeskripsikan instruksi perilaku LLM selanjutnya.

---

## 1. `GET /api/v1/flow/obsbakat/step1`
**Purpose:** Menginisiasi wawancara *Talent Mapping*.

- **Backend Action:** 
  - Mengembalikan instruksi bagi AI untuk menyapa dengan antusias.
  - Meminta AI untuk menanyakan 1-2 pertanyaan pemancing tentang hobi.

---

## 2. `GET /api/v1/flow/obsbakat/step2`
**Purpose:** Menangkap *Personal Data* dan transisi ke analisis mendalam.

- **Backend Action:**
  - Menerima konfirmasi bahwa sesi wawancara berlanjut.
  - Mengembalikan instruksi agar AI menanyakan Nama, Usia, dan Organisasi.
  - Mengarahkan AI agar segera memanggil `/step3` jika data sudah lengkap.

---

## 3. `GET /api/v1/flow/obsbakat/step3`
**Purpose:** Proses iteratif (looping) untuk *funneling* 40 Pilar Bakat.

- **Backend Action:**
  - Endpoint paling kritikal. Backend membaca `data3.json`.
  - Mengembalikan prompt yang meminta AI menggali lebih dalam membedakan hobi vs potensi nyata.
  - Meminta AI untuk memilih beberapa "Profesi" dari `data_profesi.json`.
  - Setelah wawancara dirasa cukup mengerucut, AI dipandu memanggil `/step4`.

---

## 4. `GET /api/v1/flow/obsbakat/step4`
**Purpose:** Penyajian laporan akhir (Personal Curriculum).

- **Backend Action:**
  - Menginstruksikan AI untuk mempresentasikan kesimpulan.
  - Mengkaitkan potensi anak dengan aktivitas nyata yang dikuasai.
  - Menyusun daftar profesi potensial, mengkorelasikan pilar yang kuat, dan memberi tahu pilar mana yang perlu diperbaiki (`lebih_perbaiki`, `lalai_perbaiki`).
  - Memberikan rekomendasi MVP (Minimum Viable Product) bertingkat (Beginner -> Advanced) agar anak bisa mulai berkarya.
