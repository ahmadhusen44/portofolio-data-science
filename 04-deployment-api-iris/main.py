"""
API sederhana untuk deploy model klasifikasi bunga Iris.

CARA MENJALANKAN:
1. Pastikan file 'model_iris.keras' dan 'scaler_iris.pkl' ada di folder yang
   sama dengan file ini. Kedua file itu dihasilkan dari script
   klasifikasi_iris.py yang sudah kamu buat sebelumnya (jalankan dulu script
   itu kalau belum pernah, supaya file model & scaler-nya ter-generate).
2. Install dependency (kalau belum): pip install fastapi uvicorn tensorflow joblib
3. Jalankan API dengan perintah:  uvicorn main:app --reload
4. Buka browser ke http://127.0.0.1:8000/docs untuk mencoba API secara
   interaktif (FastAPI otomatis membuatkan dokumentasi ini, tidak perlu
   dibuat manual).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import joblib
import tensorflow as tf

# 1. Load Model & Scaler (dilakukan SEKALI saat API pertama kali dijalankan,
# bukan setiap kali ada request masuk -- supaya API cepat merespons)
try:
    model = tf.keras.models.load_model("model_iris.keras")
    scaler = joblib.load("scaler_iris.pkl")
except Exception as e:
    raise RuntimeError(
        "Gagal load model/scaler. Pastikan 'model_iris.keras' dan "
        "'scaler_iris.pkl' ada di folder yang sama dengan file ini, dan "
        "sudah dihasilkan dari klasifikasi_iris.py. Detail error: " + str(e)
    )

nama_bunga = ["setosa", "versicolor", "virginica"]

# 2. Buat Aplikasi FastAPI
app = FastAPI(
    title="API Klasifikasi Bunga Iris",
    description="Prediksi jenis bunga iris berdasarkan ukuran kelopak & mahkota",
    version="1.0.0"
)

# Izinkan frontend (file HTML atau domain lain) memanggil API ini.
# Untuk portofolio/belajar, "*" (semua origin) cukup aman. Kalau nanti API ini
# dipakai untuk aplikasi produksi sungguhan, sebaiknya ganti "*" dengan domain
# frontend yang spesifik demi keamanan.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Skema Input
# Pydantic otomatis memvalidasi tipe data & memberi pesan error yang jelas
# kalau user mengirim data yang salah format (misal teks bukan angka).
class DataBunga(BaseModel):
    panjang_kelopak: float = Field(..., gt=0, description="Panjang sepal (cm)")
    lebar_kelopak: float = Field(..., gt=0, description="Lebar sepal (cm)")
    panjang_mahkota: float = Field(..., gt=0, description="Panjang petal (cm)")
    lebar_mahkota: float = Field(..., gt=0, description="Lebar petal (cm)")

    class Config:
        json_schema_extra = {
            "example": {
                "panjang_kelopak": 5.1,
                "lebar_kelopak": 3.5,
                "panjang_mahkota": 1.4,
                "lebar_mahkota": 0.2
            }
        }


# 4. Endpoint Utama
@app.get("/")
def beranda():
    """Endpoint dasar untuk cek apakah API hidup."""
    return {"pesan": "API Klasifikasi Iris aktif. Buka /docs untuk mencoba."}


@app.post("/predict")
def prediksi_bunga(data: DataBunga):
    """
    Terima 4 ukuran bunga, kembalikan prediksi jenis bunga & tingkat keyakinan.
    """
    try:
        # Susun input jadi format array 2D, sesuai yang diharapkan model
        ukuran = np.array([[
            data.panjang_kelopak,
            data.lebar_kelopak,
            data.panjang_mahkota,
            data.lebar_mahkota
        ]])

        # WAJIB pakai scaler yang SAMA dengan waktu training, bukan scaler baru
        ukuran_scaled = scaler.transform(ukuran)

        prediksi = model.predict(ukuran_scaled, verbose=0)
        indeks_prediksi = int(np.argmax(prediksi))
        jenis = nama_bunga[indeks_prediksi]
        keyakinan = float(np.max(prediksi))

        return {
            "jenis_bunga": jenis,
            "tingkat_keyakinan": round(keyakinan * 100, 2),
            "detail_probabilitas": {
                nama_bunga[i]: round(float(prediksi[0][i]) * 100, 2)
                for i in range(len(nama_bunga))
            }
        }
    except Exception as e:
        # Kembalikan error yang jelas ke pengguna API, bukan cuma crash diam-diam
        raise HTTPException(status_code=400, detail=f"Gagal memproses input: {str(e)}")