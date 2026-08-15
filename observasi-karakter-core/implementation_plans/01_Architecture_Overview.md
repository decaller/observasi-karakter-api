# 01. Architecture Overview (FastAPI)

## Core Philosophy: API-Driven AI
Aplikasi ini dirancang sebagai *Stateful API backend* yang memandu *Large Language Models* (seperti ChatGPT/Claude) layaknya klien konvensional (misalnya Vue/React). 
Daripada menyimpan seluruh logika di dalam satu *System Prompt* raksasa yang statis dan kaku, backend kita menggunakan prinsip RESTful API untuk memberikan instruksi kepada AI langkah demi langkah (Step 1, Step 2, dst).

## Backend Framework
Target pengembangan backend ini adalah menggunakan **FastAPI (Python)**. 
Keuntungan menggunakan FastAPI untuk proyek ini:
- **Pydantic Validation**: AI sering mengalami halusinasi dan dapat mengirim *query parameter* yang salah. Pydantic akan memvalidasi *request* secara otomatis.
- **Asynchronous**: Karena interaksi dengan AI dan *database* memakan waktu tunggu (*I/O bound*), *async/await* bawaan FastAPI sangat ideal.
- **Python Ecosystem**: Penggunaan Python memudahkan integrasi di masa depan jika kita ingin menggunakan NLP/Machine Learning lokal untuk analisis observasi.

## Database Architecture
Struktur data dirancang highly-relational (walaupun saat ini berformat JSON Mockup):

1. **`data3.json` (Knowledge Base Bakat)**
   - Berisi 40 Pilar Bakat.
   - Mengandung penjelasan kekuatan, kelemahan, dan relasi ID (seperti `lebih_perbaiki_ids` dan `lalai_perbaiki_ids`).

2. **`data_profesi.json` (Pemetaan Karir)**
   - Berisi daftar profesi dan jurusan kuliah.
   - Dipisahkan dari `data3` agar *scalable*.
   - Setiap profesi memiliki referensi/pemetaan balik ke ID pilar (`data3`) yang mendukung profesi tersebut.

3. **`data_karakter.json` (Observasi Karakter)**
   - Berisi 45 indikator perilaku yang dikelompokkan menjadi 15 sub-kategori spesifik (seperti "Termotivasi dalam beribadah", "Mampu bersosial").
   - Digunakan sebagai landasan skor kesiapan *baligh*.

## Routing & Global Prompting (`llms.txt`)
Frontend hanya perlu mengumpankan file `llms.txt` kepada AI sebagai instruksi utama (System Prompt).
Di dalam file tersebut, terdapat *routing logic* sederhana:
- Jika konteksnya **Observasi Bakat**, AI diinstruksikan untuk memanggil `/result/v1/flow/obsbakat/step1`.
- Jika konteksnya **Observasi Karakter**, AI diinstruksikan untuk memanggil `/result/v1/flow/obskarakter/step1_wawancara`.
Frontend dapat menyuntikkan variabel (seperti `{{TARGET_NAMA}}` atau `{{OBSERVASI_TIPE}}`) secara dinamis ke dalam file ini sebelum dikirim ke LLM.
