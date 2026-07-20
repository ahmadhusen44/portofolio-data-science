# ETL Pipeline & Analisis SQL — Segmentasi Pelanggan Mall

## Tujuan
Belajar proses data engineering dasar: memindahkan data dari file mentah (CSV) ke database yang terstruktur, lalu menganalisisnya pakai SQL tingkat menengah (JOIN, window function, CTE).

## Struktur Proyek
- `schema.sql` — desain database (2 tabel ternormalisasi: `pelanggan` & `profil_belanja`)
- `etl_pipeline.py` — script Extract-Transform-Load dari CSV ke MySQL
- `queries_analitis.sql` — 7 query analitis, dari dasar sampai window function & CTE
- `Mall_Customers.csv` — data mentah (sama dengan yang dipakai di proyek clustering)

## Cara Menjalankan

1. **Buat database & tabel**: jalankan `schema.sql` di MySQL Workbench/phpMyAdmin
2. **Sesuaikan kredensial** di `etl_pipeline.py` (bagian `KONFIGURASI_DB`)
3. **Install dependency**: `pip install pandas mysql-connector-python`
4. **Jalankan ETL**: `python etl_pipeline.py`
5. **Coba query analitis**: buka `queries_analitis.sql`, jalankan satu-satu di MySQL untuk lihat hasilnya

## Kenapa Data Dipecah Jadi 2 Tabel (Bukan 1 Tabel Flat)?

CSV aslinya cuma 1 tabel flat. Saya sengaja memisahkannya jadi `pelanggan` (data demografis) dan `profil_belanja` (data perilaku), dihubungkan lewat `customer_id`, untuk latihan:
- Desain skema yang lebih dekat dengan praktik nyata (data jarang datang sebagai 1 tabel rapi)
- Latihan `JOIN` yang sebenarnya, bukan cuma teori
- Memahami kapan data *sebaiknya* dipisah (kategori informasi berbeda) vs kapan lebih baik digabung

## Insight dari Query Analitis

Beberapa hal yang saya pelajari saat menulis query-query ini:
- **Window function (`RANK() OVER PARTITION BY`)** beda dari `ORDER BY` biasa — ranking-nya "reset" untuk tiap kelompok (misal per gender), bukan ranking global
- **CTE (`WITH ... AS`)** membuat query kompleks jadi lebih mudah dibaca, dibanding subquery bersarang yang membingungkan
- **NTILE(4)** berguna untuk membagi data jadi kuartil (25% teratas, dst) tanpa perlu hitung manual — ini yang saya pakai untuk cari pelanggan "premium" (income & spending sama-sama di 25% teratas)

## Hasil Menjalankan Query (Update Setelah Dicoba)

**JOIN & GROUP BY (Query #1-2)**: data pelanggan & profil belanja tergabung dengan benar lewat `customer_id`. Ditemukan pola menarik per gender:
- **Female**: 112 pelanggan, rata-rata spending score **51.53** (lebih tinggi)
- **Male**: 88 pelanggan, rata-rata income **62.23** (lebih tinggi)

Artinya walau pelanggan pria rata-rata pendapatannya lebih tinggi, pelanggan wanita justru lebih banyak berbelanja secara proporsional — insight ini bisa langsung dipakai untuk strategi promosi yang dibedakan per gender.

**Window function `RANK()` (Query #4)**: menunjukkan cara `RANK()` menangani nilai seri (*tied values*) — kalau ada 2 pelanggan dengan spending score sama, keduanya dapat ranking sama, tapi ranking berikutnya "melompati" angka sesuai jumlah baris yang seri (bukan `DENSE_RANK()` yang tidak melompat).

**Window function tanpa PARTITION BY (Query #5)**: kolom rata-rata (`50.20`) sama persis di semua baris, karena dihitung dari SELURUH data — beda dengan Query #4 yang pakai `PARTITION BY gender` sehingga nilainya beda-beda per kelompok. Ini perbandingan konkret yang membantu saya paham kapan `PARTITION BY` diperlukan.

**Subquery (Query #7)**: 97 dari 200 pelanggan (hampir setengah) punya spending score di atas rata-rata — wajar secara statistik untuk distribusi yang relatif simetris.

**Validasi silang dengan proyek clustering (Query #6, CTE + NTILE)**: pelanggan yang teridentifikasi sebagai "premium" lewat query SQL murni (income & spending sama-sama di kuartil teratas) — misalnya `customer_id 200` (income 137k$, spending 83) — ternyata **konsisten** dengan pelanggan yang masuk cluster "premium" di proyek clustering K-Means (`03-clustering-segmentasi-pelanggan`). Dua pendekatan berbeda total (SQL manual vs machine learning) menghasilkan kesimpulan yang sama — ini validasi silang yang meyakinkan bahwa segmen "pelanggan premium" ini memang pola nyata di data, bukan artefak dari satu metode saja.

Pelanggan `customer_id 12` dan `20` juga menarik dicatat — mereka konsisten muncul di posisi ekstrem (ranking teratas) di hampir semua query berbeda (ranking per gender, selisih dari rata-rata, subquery di atas rata-rata), menunjukkan mereka memang outlier yang jelas dalam pola spending.

## Latihan Mandiri (TODO)
- [ ] Bandingkan hasil `RANK()` vs `DENSE_RANK()` pada Query #4 — perhatikan bagaimana keduanya menangani nilai yang seri (tied values) secara berbeda