# Global Architecture Documentation

Dokumen perencanaan teknis untuk backend (FastAPI) observasi ini kini telah dipecah menjadi beberapa dokumen spesifikasi modular agar lebih mendalam dan terfokus untuk diimplementasikan oleh *developer*. 

Silakan merujuk pada file-file berikut di dalam folder `implementation_plans/`:

1. [01. Architecture Overview (FastAPI)](file:///home/abuhafi/Project/observasi-karakter-api/observasi-karakter-core/implementation_plans/01_Architecture_Overview.md)
   - Konsep *Stateful API*, struktur database, dan *routing*.
2. [02. Observasi Bakat API Spec](file:///home/abuhafi/Project/observasi-karakter-api/observasi-karakter-core/implementation_plans/02_Obsbakat_API_Spec.md)
   - Spesifikasi alur 4 langkah untuk *Talent Mapping*.
3. [03. Observasi Karakter API Spec](file:///home/abuhafi/Project/observasi-karakter-api/observasi-karakter-core/implementation_plans/03_Obskarakter_API_Spec.md)
   - Spesifikasi wawancara 15 sub-kategori, skoring, analisis kesiapan baligh, dan transisi antar produk.
4. [04. Prompting Strategy & Fallback Handling](file:///home/abuhafi/Project/observasi-karakter-api/observasi-karakter-core/implementation_plans/04_Prompting_Strategy.md)
   - Penjelasan teknis tentang penginjeksian variabel global (`llms.txt`), pentingnya penggunaan *emoji*, serta teknik *self-correction* AI menggunakan validasi ketat Pydantic dari FastAPI.

---
*Catatan: Segala pembaruan strategi arsitektur di masa mendatang hendaknya dicatat pada dokumen yang sesuai di atas.*
