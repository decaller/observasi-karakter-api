# 04. Prompting Strategy & Fallback Handling

Karena inti aplikasi ini adalah memberikan instruksi ke LLM (ChatGPT/Claude), maka metode *Prompting* sangat krusial. Sistem API yang kita kembangkan menggunakan arsitektur pemisahan *Prompt* agar hemat *token* dan fokus pada tugas *(task-oriented)*.

## Variabel Global (Injeksi Frontend)
Agar API tidak perlu menanyakan informasi awal kepada *User*, file utama `mockup/llms.txt` bertindak sebagai gerbang (Router). Frontend akan melakukan penggantian string dinamis (Injeksi) pada variabel berikut sebelum memberikannya ke AI:

- `{{TARGET_NAMA}}`: Nama individu yang diobservasi.
- `{{OBSERVASI_TIPE}}`: Apakah ini evaluasi untuk 'Diri Sendiri' atau evaluasi 'Anak'. (Ini akan mengubah gaya bahasa AI antara sudut pandang pertama vs sudut pandang ketiga).

## Struktur Prompt API per Fase (Step)
Setiap panggilan ke API backend FastAPI (seperti `/step1`, `/step2`) akan selalu membalas dengan struktur JSON berstandar ganda:

1. **`present_result_prompt`**: Teks yang memberi tahu AI bagaimana merespons, memuji, atau menyajikan data di layar dari percakapan sebelumnya.
2. **`next_prompt_hint`**: Arahan taktis untuk "langkah selanjutnya". Bagian ini sangat penting karena memuat panduan gaya bahasa (seperti penggunaan *emoji* ramah, sikap konseling santai) dan parameter-parameter kapan AI harus *stop* serta memanggil endpoint berikutnya.

## Mitigasi Hallucination & Validasi Pydantic
Karena LLM mengkonstruksi URL API secara mandiri (melalui Tool Calling), ia rentan mengalami halusinasi (misal mengirim `?umur=dua puluh` padahal di API diminta integer `?umur=20`).

Untuk memitigasi ini, struktur FastAPI harus menggunakan Pydantic untuk `Request Model` yang ketat. Jika AI salah mengisi format parameter, FastAPI akan otomatis membalas dengan Error 422 (Unprocessable Entity) beserta pesan kesalahan yang jelas dari Pydantic (contoh: `"umur must be an integer"`). LLM pintar (seperti GPT-4 / Claude-3.5) akan dapat membaca pesan error HTTP ini secara otomatis (Self-Correction) lalu mengulangi panggilan API dengan format yang benar.

## Pentingnya Emoji 💬
Di semua *mockup prompt* kita (seperti `step1_wawancara.json`), penggunaan Emoji diinstruksikan secara eksplisit. Hal ini tidak hanya mempercantik *output* di layar klien, tapi juga secara psikologis menempatkan perilaku (persona) AI menjadi jauh lebih empatik, hangat, dan sangat cocok untuk interaksi bertema konseling maupun *parenting*.
