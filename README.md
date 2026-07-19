# Portofolio Data Science — Achmad Chusen

Mahasiswa Sistem Informasi | Belajar data science secara mandiri

Kumpulan proyek ini dimulai dari latihan fondasi (data wrangling & visualisasi), lalu berkembang ke empat area inti data science: regresi, klasifikasi, clustering, dan deployment model jadi API. Setiap proyek disertai penjelasan proses berpikir, termasuk kesalahan yang saya temui dan cara mengatasinya — karena bagian itu yang menurut saya paling menunjukkan cara saya bekerja, bukan cuma hasil akhirnya.

---

## 📁 Struktur Proyek

```
portofolio-data-science/
├── 00-dasar-data-wrangling-visualisasi/
│   ├── bersih_data.py
│   └── visualisasi_iris.py
├── 01-regresi-harga-rumah/
│   └── analisis_california.py
├── 02-klasifikasi-iris/
│   └── klasifikasi_iris.py
├── 03-clustering-segmentasi-pelanggan/
│   └── segmentasi_pelanggan_mall.py
├── 04-deployment-api-iris/
│   ├── main.py
│   ├── index.html
│   ├── requirements.txt
│   ├── Procfile
│   └── PANDUAN_DEPLOYMENT.md
└── README.md   <- file ini
```

---

## 0️⃣ Fondasi — Data Wrangling & Visualisasi

Latihan paling awal saya sebelum masuk ke pemodelan machine learning: memahami cara menangani data yang tidak lengkap, dan cara membaca pola data lewat visualisasi.

**`bersih_data.py`** — membandingkan dua pendekatan menangani *missing values*:
- **Dropna**: menghapus baris yang datanya tidak lengkap — sederhana, tapi berisiko membuang informasi kalau missing value-nya banyak
- **Imputasi (fillna dengan mean)**: mengisi nilai kosong dengan rata-rata kolom — mempertahankan jumlah data, tapi bisa menyesatkan kalau data yang tersisa untuk dihitung rata-ratanya terlalu sedikit atau distribusinya tidak simetris (di kasus ini, kolom Gaji cuma punya 2 dari 6 nilai asli, jadi mean-nya kurang representatif — pelajaran yang saya ambil: pilihan dropna vs imputasi tidak selalu jelas mana yang lebih benar, tergantung konteks data)

**`visualisasi_iris.py`** — eksplorasi dataset Iris memakai Seaborn:
- **Scatterplot** untuk melihat hubungan dua variabel per spesies
- **Pairplot** untuk melihat hubungan semua variabel sekaligus — cara cepat mengenali pola sebelum membuat model
- **Boxplot** untuk melihat sebaran data dan mendeteksi outlier

Latihan ini jadi fondasi penting sebelum saya masuk ke proyek klasifikasi Iris yang lebih lengkap di folder `02`.

---

## 1️⃣ Regresi — Prediksi Harga Rumah (California Housing)

**Masalah**: memprediksi harga rumah median berdasarkan karakteristik area (pendapatan, usia rumah, lokasi, dll).

**Model**: Linear Regression vs Random Forest Regressor — dibandingkan langsung untuk melihat mana yang lebih baik menangkap hubungan non-linear di data ini.

**Hasil**: Random Forest jauh lebih unggul (MAE ~0.33 vs ~0.53, dalam satuan $100,000), menunjukkan hubungan antar fitur dan harga rumah memang tidak sepenuhnya linear.

**Insight menarik**: `MedInc` (pendapatan) adalah fitur paling berpengaruh (~52%), diikuti `AveOccup` dan lokasi geografis (Latitude/Longitude).

**Pelajaran penting yang saya temui**: pada percobaan awal saya secara tidak sengaja memasukkan variabel target ke dalam daftar fitur, menyebabkan **data leakage** — model "mencontek" jawabannya sendiri, menghasilkan error yang tampak sempurna (MAE = 0) tapi sebenarnya tidak berguna. Ini pelajaran penting: metrik yang tampak "terlalu bagus" justru harus dicurigai, bukan langsung dirayakan.

---

## 2️⃣ Klasifikasi — Jenis Bunga Iris

**Masalah**: mengklasifikasikan spesies bunga iris (setosa, versicolor, virginica) berdasarkan ukuran kelopak dan mahkota.

**Model**: Neural network sederhana (2 hidden layer) dengan TensorFlow/Keras.

**Hasil**: akurasi 100% pada data test — wajar untuk dataset ini karena ukurannya kecil dan pola antar spesies memang terpisah jelas, bukan indikasi overfitting/leakage seperti kasus regresi di atas.

**Fitur teknis**: model dan scaler disimpan (`model.save()`, `joblib.dump()`) supaya tidak perlu training ulang setiap kali dipakai, dan supaya scaler yang dipakai saat prediksi konsisten dengan yang dipakai saat training.

---

## 3️⃣ Clustering — Segmentasi Pelanggan Mall

**Masalah**: mengelompokkan pelanggan mall ke beberapa segmen berdasarkan usia, pendapatan tahunan, dan spending score — **tanpa label**, murni pembelajaran tak terarah (unsupervised).

**Teknik**: K-Means, dengan penentuan jumlah cluster optimal lewat *elbow method* dan *silhouette score* (K=5 terbukti optimal, silhouette score 0.55). Dilanjutkan dengan PCA untuk meringkas 3 fitur jadi 2 dimensi agar bisa divisualisasikan.

**Insight bisnis**: teridentifikasi 5 segmen pelanggan, di antaranya "income tinggi & belanja tinggi" (target utama promosi) dan "income tinggi & belanja rendah" (perlu strategi berbeda untuk menarik minat belanja).

**Interpretasi PCA**: loading menunjukkan PC1 merepresentasikan pola usia-vs-belanja, sementara PC2 hampir sepenuhnya mencerminkan tingkat pendapatan — membantu memahami apa sebenarnya yang direpresentasikan tiap sumbu di visualisasi.

---

## 4️⃣ Deployment — API Klasifikasi Iris

**Tujuan**: membawa model dari sekadar script/notebook menjadi layanan yang bisa diakses aplikasi lain lewat HTTP request — simulasi bagaimana model dipakai di dunia kerja nyata.

**Stack**: FastAPI (dengan validasi input otomatis via Pydantic) + frontend HTML sederhana untuk mencoba prediksi tanpa perlu tools teknis seperti Postman.

**Fitur**:
- Endpoint `POST /predict` menerima 4 ukuran bunga, mengembalikan prediksi + tingkat keyakinan per kelas
- Dokumentasi interaktif otomatis di `/docs` (bawaan FastAPI)
- CORS diaktifkan supaya frontend HTML bisa memanggil API dari origin berbeda
- Sudah diuji lewat 3 cara berbeda: Swagger UI, `curl`, dan PowerShell `Invoke-RestMethod` — semuanya konsisten

**Cara menjalankan lokal**: lihat komentar di `main.py`. Untuk deploy ke cloud, ikuti `PANDUAN_DEPLOYMENT.md`.

---

## 🛠️ Tools & Library yang Dipakai
Python, Pandas, NumPy, Scikit-learn, TensorFlow/Keras, Seaborn, Matplotlib, FastAPI, Uvicorn, Pydantic, Joblib

## 📌 Rencana Selanjutnya
- [ ] Deploy API ke Render (lihat panduan di folder 04)
- [ ] Tambah proyek klasifikasi dengan dataset yang lebih "kotor"/realistis
- [ ] Eksplorasi deep learning untuk kasus computer vision/NLP

---

*Kalau ada pertanyaan soal proyek-proyek ini, jangan ragu untuk menghubungi saya di [https://www.Linkedin.com/in/ahmad-husen-4976a0325].*