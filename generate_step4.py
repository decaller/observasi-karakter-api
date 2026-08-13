import json

with open('mockup/data3.json', 'r') as f:
    data3 = json.load(f)

with open('mockup/data_profesi.json', 'r') as f:
    data_profesi = json.load(f)

chosen_professions = ["Programmer", "Penulis"]

result = {
    "session_id": "sess_abc123",
    "chosen_professions": [],
    "present_result_prompt": "Anda adalah konsultan karir. Berikut adalah data pilar yang berkaitan dengan profesi pilihan pengguna beserta skor mereka saat ini. 1. Buat breakdown aktivitas yang harus dikuasai untuk masing-masing profesi. 2. Hubungkan aktivitas tersebut dengan pilar yang ada di data. 3. Tampilkan skor saat ini untuk menunjukkan apakah pengguna kemungkinan bisa menguasai aktivitas tersebut dengan mudah atau butuh usaha lebih. 4. Urutkan profesi dari yang paling mungkin dikuasai hingga yang paling sulit. Untuk setiap profesi, tunjukkan pilar apa yang masih kurang (skor < 70) dan berikan saran bagaimana cara memperkuatnya menggunakan data 'lalai_perbaiki' atau 'lebih_perbaiki' yang tersedia. MAKSIMALKAN format Markdown Anda (Gunakan tabel, blok kutipan, dan warna/emoji) agar presentasi ini terlihat sangat elegan dan profesional.",
    "next_action": {
        "type": "choose_mvp_profession"
    },
    "next_prompt_hint": "Dari profesi yang sudah dianalisis di atas, tanyakan kepada pengguna mana SATU profesi yang ingin mereka buatkan Kurikulum MVP (Minimum Viable Product) secara detail. Setelah mereka menjawab, buatkan 1. Tingkatan level proyek MVP dari beginner hingga advanced untuk profesi tersebut. 2. Soroti pendidikan tinggi atau jurusan yang relevan untuk mendukung proyek MVP tersebut. Anda tidak perlu memanggil API lagi untuk melakukan ini, cukup gunakan pengetahuan Anda sendiri yang dihubungkan dengan pilar yang sudah kita temukan."
}

mock_scores = {
    "10": 88,
    "11": 92,
    "12": 65,
    "4": 78,
    "5": 82,
    "20": 45,
}

for prof in chosen_professions:
    prof_data = {
        "name": prof,
        "related_pillars": [],
        "related_jurusans": []
    }
    
    # Get from data_profesi
    if prof in data_profesi:
        prof_data["related_jurusans"] = data_profesi[prof]["related_jurusans"]
        for p_id in data_profesi[prof]["related_pillars"]:
            # Find the pillar in data3
            for key, val in data3.items():
                if str(val.get("pilar40", key)) == p_id:
                    score = mock_scores.get(p_id, 80)
                    prof_data["related_pillars"].append({
                        "id": p_id,
                        "name": val.get("nama_lengkap", f"Pilar {p_id}"),
                        "score": score,
                        "lalai_definisi": val.get("lalai_definisi", ""),
                        "lalai_perbaiki": val.get("lalai_perbaiki", ""),
                        "lalai_perbaiki_ids": val.get("lalai_perbaiki_ids", []),
                        "lebih_definisi": val.get("lebih_definisi", ""),
                        "lebih_perbaiki": val.get("lebih_perbaiki", ""),
                        "lebih_perbaiki_ids": val.get("lebih_perbaiki_ids", [])
                    })
                    break

    result["chosen_professions"].append(prof_data)

with open('mockup/step4.json', 'w') as f:
    json.dump(result, f, indent=2)

print("Generated step4.json successfully!")
