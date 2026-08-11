# Workflow Diagram

Below is the Mermaid representation of your workflow diagram, divided into Pertanyaan (User Inputs/Questions) and Proses (System Processing/Outputs).

```mermaid
graph TD
    subgraph Pertanyaan ["Pertanyaan (User Input)"]
        Q1["Introvert / Ekstrovert ?"]
        Q2["Urutkan Ego:<br/>Tinggi - Sedang - Rendah!"]
        Q3["Urutkan 3 sifat dari<br/>masing-masing 6 kategori!"]
        Q4["Cek 2/3/4 pernyataan<br/>untuk masing-masing 18 kategori<br/>(setuju / ubah)"]
        Q5["Pilih Profesi yg paling<br/>diminati dari pilihan"]
        Q6["Pilih Aktivitas terkait<br/>profesi yg belum dikuasai"]
    end

    subgraph Proses ["Proses (AI / System)"]
        P1["Urutkan 6 Kategori Bakat"]
        P2["Tampilkan:<br/>Sulukan, Gaya Belajar & Bahasa Hati"]
        P3["Hitung nilai default<br/>setiap 40 bakat"]
        P4["Tampilkan:<br/>Preview dari Bagan Pohon"]
        P5["Tampilkan:<br/>Laporan Lengkap"]
        P6["Rangkum & Olah Aktivitas<br/>& Profesi Paling Cocok"]
        P7["Ramu jalur pendidikan<br/>dengan MVP milestone"]
        P8["Laporan Kurikulum Personalisasi"]
    end

    %% Flow Connections
    Q1 --> Q2
    Q2 --> P1
    P1 --> P2
    P2 --> Q3
    Q3 -. Loop (6 Kategori) .-> Q3
    Q3 --> P3
    P3 --> P4
    P4 --> Q4
    Q4 -. Loop (18 Kategori) .-> Q4
    Q4 --> P5

    %% Phase 2 (Below the dashed line)
    P5 --> P6
    P6 --> Q5
    Q5 --> Q6
    Q6 --> P7
    P7 --> P8
```

## Workflow Summary

- **Personality & Ego Intake**: User specifies Introvert/Ekstrovert and ranks Ego level.
- **Talent Category Ranking**: System ranks 6 talent categories and outputs learning style & preferences (Sulukan, Gaya Belajar & Bahasa Hati).
- **Trait Ranking & Scoring**: User ranks 3 traits across 6 categories (iterative loop), triggering calculation for 40 talent default values and displaying a tree chart preview (Bagan Pohon).
- **Statement Verification**: User verifies statements across 18 categories (iterative loop), producing the complete report (Laporan Lengkap).
- **Career & Activity Matching**: System summarizes best-fit activities/professions. User selects preferred professions and unmastered skills.
- **Curriculum Generation**: System creates an MVP milestone educational path resulting in a Personalized Curriculum Report (Laporan Kurikulum Personalisasi).