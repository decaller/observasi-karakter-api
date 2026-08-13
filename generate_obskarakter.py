import json
import os

os.makedirs('mockup/obskarakter', exist_ok=True)

data = {
    "I. KARAKTER IMAN": {
        "A. AQIDAH": [
            "Anak tidak perlu disuruh ketika akan melakukan ibadah sholat.",
            "Meskipun tanpa tekanan, anak tetap berkata jujur, dan juga bukan karena takut kepada orang tua, guru, atau orang lain.",
            "Anak tidak harus diingatkan untuk menerapkan tuntunan adab pada aktifitas hariannya.",
            "Anak sering membicarakan tentang surga atau neraka.",
            "Anak sering mengingatkan atau berkomentar kepada saudara, teman, atau orang lain yang melakukan pelanggaran syariat.",
            "Anak tidak marah (berbesar hati) jika dibangunkan untuk melaksanakan sholat subuh.",
            "Anak tidak sembunyi-sembunyi agar tidak diketahui orang tua atau gurunya, ketika anak akan bermain HP atau permainan lainnya.",
            "Anak sering mengucapkan dzikir tertentu ketika mengalami sesuatu kejadian yang menyenangkan maupun yang tidak menyenangkan.",
            "Anak mengembalikan kepada yang memiliki atau menyerahkan kepada orangtua/guru, ketika anak menemukan uang atau barang yang bukan miliknya."
        ],
        "B. IBADAH": [
            "Anak sering membaca atau mendengarkan Al qur’an.",
            "Anak sering melakukan muroja’ah hafalan Al Qur’an.",
            "Tata caranya sudah benar, ketika anak melaksanakan wudhu.",
            "Anak sering melaksanakan aktifitas ibadah sholat wajib.",
            "Tata caranya sudah benar, ketika anak melaksanakan sholat.",
            "Anak sering menerapkan tata cara adab Islami dalam aktifitas hariannya.",
            "Anak sering mengajak saudara atau teman untuk melaksanakan ibadah.",
            "Anak ikut aktif dalam kegiatan ibadah bulan Ramadhan.",
            "Anak dapat mempraktekkan tata cara tayamum."
        ],
        "C. KEMANDIRIAN": [
            "Anak siap menikah karena anak merasa sudah mampu menghidupi keluarga.",
            "Anak mampu membiayai hidupnya sendiri dari penghasilan yang anak dapatkan.",
            "Anak mampu menanggung biaya pendidikannya sendiri.",
            "Anak mampu merencanakan dan mengatur keuangannya sendiri.",
            "Anak mampu mengurus kebutuhan pribadinya tanpa bantuan orang lain seperti mandi, mencuci pakaian, menyiapkan makanan.",
            "Anak dapat mengatur waktu dengan baik untuk menyelesaikan tugas-tugas atau pekerjaannya.",
            "Anak memiliki pemahaman yang baik tentang kesehatan pribadi dan menerapkan gaya hidup sehat.",
            "Anak mampu mengatasi stres dan tekanan dalam hidup anak dengan baik.",
            "Anak mampu bersosial dengan baik sehingga anak diterima oleh masyarakat sekitarku."
        ]
    },
    "II. KARAKTER BELAJAR": [
        "Anak tidak perlu disuruh untuk belajar.",
        "Anak berusaha menemukan solusi ketika menghadapi kesulitan (dalam bermain atau dalam kondisi lainnya).",
        "Anak tidak canggung atau tidak malu untuk bertanya kepada orang yang tidak dikenal, ketika anak ingin menanyakan arah jalan atau sesuatu yang belum diketahuinya.",
        "Anak sering memanfaatkan benda-benda sekitar untuk media/obyek belajarnya.",
        "Anak sering menjelajah lingkungan sekitar atau tempat-tempat tertentu untuk menuntaskan rasa ingin tahunya.",
        "Anak banyak bertanya kepada orang tua, guru, atau orang lain tentang sesuatu hal yang tidak diketahuinya.",
        "Anak sering berusaha keras untuk mencoba melakukan sesuatu yang belum pernah dilakukannya.",
        "Tanpa ada rasa takut salah atau takut disalahkan, ketika anak mencoba melakukan sesuatu.",
        "Anak sering lupa waktu ketika sedang mempelajari sesuatu yang belum diketahuinya."
    ],
    "III. KARAKTER BAKAT": [
        "Anak memiliki sifat tertentu yang menjadikan dirinya berbeda dengan lainnya.",
        "Anak memiliki permainan atau aktifitas khusus yang sangat disukainya dan favorit baginya.",
        "Anak mampu melakukan/membuat dengan baik sehingga hasilnya bagus, terhadap permainan/aktifitas favoritnya.",
        "Anak berulang-ulang melakukan, terhadap permainan/aktifitas favoritnya.",
        "Tanpa persiapan matang (spontanitas), anak dapat melakukan permainan/aktifitas favoritnya dengan baik.",
        "Anak dapat memanfaatkan barang mainan buatan sendiri.",
        "Meskipun menghadapi kesulitan, anak tidak putus asa untuk tetap berusaha menyelesaikan mainan/aktifitas favoritnya.",
        "Meskipun sering gagal, anak tetap mencoba menyelesaikan mainan/aktivitas favoritnya.",
        "Untuk mendapatkan mainan atau untuk dapat melakukan aktifitas favoritnya, anak rela menabung uang jajannya."
    ]
}

with open('mockup/obskarakter/data_karakter.json', 'w') as f:
    json.dump(data, f, indent=2)

step1_wawancara = {
    "session_id": "char_abc123",
    "indicators_to_evaluate": data,
    "present_result_prompt": "Anda adalah Konselor Karakter. Berdasarkan data 45 indikator yang telah di-load di memori Anda, buatlah sebuah skenario wawancara cerita yang sangat natural. JANGAN menyajikan daftar indikator kepada pengguna.",
    "next_action": {
        "type": "conduct_interview"
    },
    "next_prompt_hint": "Buka obrolan dengan menyapa pengguna. Katakan bahwa alih-alih mengisi kuesioner kaku, Anda ingin mendengarkan cerita nyata. Berikan satu pancingan pertanyaan pembuka, misalnya: 'Bisa ceritakan sedikit bagaimana rutinitas pagi hari {{TARGET_NAMA}} dari mulai bangun tidur hingga beraktivitas?' Saat pengguna bercerita, simpulkan sendiri secara laten indikator-indikator mana saja dari 45 daftar di atas yang terpenuhi. Lanjutkan percakapan santai ini maksimal 3 putaran (tanyakan hal-hal yang belum tertutup dari ceritanya). Jangan pernah memberikan list pertanyaan berurutan."
}

with open('mockup/obskarakter/step1_wawancara.json', 'w') as f:
    json.dump(step1_wawancara, f, indent=2)

print("Obskarakter mockups generated.")
