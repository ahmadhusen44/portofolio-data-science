# Panduan Deploy API ke Render (Gratis)

Render dipilih karena gratis, mendukung Python/FastAPI langsung, dan tidak perlu kartu kredit untuk tier gratisnya.

## Langkah-langkah

### 1. Upload proyek ke GitHub dulu
Pastikan folder deployment kamu (berisi `main.py`, `requirements.txt`, `model_iris.keras`, `scaler_iris.pkl`, `Procfile`) sudah di-push ke repository GitHub. Render akan mengambil kode langsung dari GitHub.

> Catatan: file model (`.keras`) biasanya berukuran kecil untuk kasus iris ini, jadi aman di-push ke GitHub. Untuk model yang jauh lebih besar (ratusan MB), biasanya perlu Git LFS — tapi untuk proyek ini tidak perlu.

### 2. Daftar & buat Web Service di Render
1. Buka [render.com](https://render.com), daftar pakai akun GitHub kamu
2. Klik **New +** → **Web Service**
3. Pilih repository GitHub yang berisi proyek API iris kamu
4. Isi konfigurasi:
   - **Name**: bebas, misalnya `api-klasifikasi-iris`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### 3. Deploy
Klik **Create Web Service**. Render akan otomatis build dan menjalankan API-nya. Proses ini bisa beberapa menit karena harus install TensorFlow.

### 4. Dapatkan URL publik
Setelah selesai, Render akan kasih URL seperti:
```
https://api-klasifikasi-iris.onrender.com
```
Coba buka `https://api-klasifikasi-iris.onrender.com/docs` — kalau muncul halaman dokumentasi yang sama seperti di localhost, berarti berhasil.

### 5. Update frontend
Buka `index.html`, ganti baris ini:
```javascript
const API_URL = "http://127.0.0.1:8000/predict";
```
menjadi URL Render kamu:
```javascript
const API_URL = "https://api-klasifikasi-iris.onrender.com/predict";
```

## Catatan penting soal tier gratis Render
- Server akan "tidur" otomatis kalau tidak ada request selama beberapa menit. Request pertama setelah tidur akan terasa lambat (~30-60 detik) karena server perlu "bangun" dulu — ini normal untuk tier gratis, bukan bug.
- Kalau kamu mau demo proyek ini secara langsung (misal saat interview), buka URL-nya beberapa menit sebelumnya supaya sudah "bangun".

## Alternatif lain
Kalau Render bermasalah, alternatif serupa: **Railway** (railway.app) atau **Fly.io** — caranya mirip (hubungkan GitHub, deploy otomatis).