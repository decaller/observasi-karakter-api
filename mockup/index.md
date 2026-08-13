# Observasi Karakter & Bakat API Mockups

Repositori ini memuat struktur JSON dan panduan API untuk menggerakkan AI dalam melakukan penilaian psikologis dan karakter.

Struktur telah dipisah menjadi dua *domain* utama:

## 1. `obsbakat/` (Observasi Bakat - 40 Pilar)
Jalur ini memetakan sifat bawaan pengguna menggunakan pendekatan 40 Pilar Karakter.
- **`step1.json`**: Menilai orientasi energi sosial dan dorongan ego dasar.
- **`step2.json` / `step2_loop_x.json`**: Memverifikasi sifat-sifat melalui kuesioner interaktif dengan kedalaman yang bisa dipilih (6, 18, atau 40 langkah).
- **`step3.json`**: Menyajikan hasil akhir dan rekomendasi karir utama.
- **`step4.json`**: Kurikulum MVP dan korelasi antara pilihan profesi dengan pilar-pilar yang masih perlu diperkuat.
- **`data3.json`**: Single Source of Truth untuk data 40 pilar psikologi.
- **`data_profesi.json`**: Database pemetaan Profesi ke Jurusan dan Pilar yang terkait.

## 2. `obskarakter/` (Observasi Pertumbuhan Karakter)
Jalur baru (berdasarkan LEMBAR OBSERVASI 1) untuk menilai adab, iman, ibadah, kemandirian, belajar, dan bakat secara kasual melalui pendekatan wawancara cerita.
- **`data_karakter.json`**: Dataset berisi 45 indikator observasi karakter.
- **`step1_wawancara.json`**: Prompt instruksi API untuk memulai wawancara naratif.

## Konfigurasi Global
Lihat `llms.txt` di root direktori ini untuk melihat instruksi sistem (System Prompt) yang mendasari AI dalam mengelola konteks wawancara untuk kedua *domain* di atas.
