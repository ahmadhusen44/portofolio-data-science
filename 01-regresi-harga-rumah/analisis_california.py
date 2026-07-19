import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# CATATAN PENTING:
# Data yang dipakai di sini SECARA ASLI adalah dataset California Housing (AS),
# bukan data rumah Jabodetabek sungguhan. Nama variabel & nama file sengaja
# diubah ke Bahasa Indonesia untuk latihan/portofolio, tapi ANGKA di dalamnya
# tetap merefleksikan kondisi California. Kalau file ini dipakai untuk
# portofolio/presentasi, jelaskan konteks ini supaya tidak menyesatkan (misalnya
# sebutkan "menggunakan dataset California Housing sebagai studi kasus").

# 1. Ambil Data
housing = fetch_california_housing(as_frame=True)
df = housing.frame  # dataframe ini sudah termasuk kolom target

# Ganti nama kolom ke Bahasa Indonesia
df = df.rename(columns={
    'MedInc': 'pendapatan',        # median pendapatan (dalam puluhan ribu USD)
    'HouseAge': 'usia_rumah',       # usia median rumah
    'AveRooms': 'rata_kamar',       # rata-rata jumlah kamar per rumah tangga
    'AveBedrms': 'rata_kamar_tidur',# rata-rata jumlah kamar tidur per rumah tangga
    'Population': 'populasi',       # populasi area
    'AveOccup': 'rata_penghuni',    # rata-rata jumlah penghuni per rumah tangga
    'Latitude': 'lintang',          # lokasi: lintang
    'Longitude': 'bujur',           # lokasi: bujur
    'MedHouseVal': 'harga_rumah'    # target: median harga rumah (dalam $100,000)
})

# 2. Cek kolom dataset
print("Kolom yang tersedia:", df.columns.tolist())

# 3. Tentukan Fitur (X) dan Target (Y)
fitur = ['pendapatan', 'usia_rumah', 'rata_kamar', 'rata_kamar_tidur',
         'populasi', 'rata_penghuni', 'lintang', 'bujur']
X = df[fitur]
y = df['harga_rumah']  # Target: harga rumah median (dalam satuan $100,000)

# 4. Bagi Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Eksperimen: Bandingkan Linear Regression vs Random Forest
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    prediksi = model.predict(X_test)
    mae = mean_absolute_error(y_test, prediksi)
    print(f"MAE untuk {name}: {mae:.4f}  (dalam satuan $100,000)")

# Simpan referensi eksplisit ke model Random Forest, jangan mengandalkan
# variabel 'model' sisa loop di atas (rapuh kalau urutan dict berubah)
model_rf = models["Random Forest"]

# Ambil feature importance dari model Random Forest
importances = model_rf.feature_importances_
for nama_fitur, skor in zip(fitur, importances):
    print(f"Pentingnya fitur {nama_fitur}: {skor:.4f}")

# 4. BAR CHART FEATURE IMPORTANCE (Melihat fitur mana yang paling berpengaruh)
# Diurutkan dari yang paling penting supaya mudah dibaca
urutan = np.argsort(importances)  # urutan ascending, biar barh dari bawah ke atas benar
fitur_urut = [fitur[i] for i in urutan]
skor_urut = [importances[i] for i in urutan]

plt.figure(figsize=(8, 6))
plt.barh(fitur_urut, skor_urut, color='#2a78d6')
plt.xlabel("Feature importance")
plt.title("Feature Importance - Random Forest (Prediksi Harga Rumah)")
plt.tight_layout()
plt.show()

# 1. HEATMAP (Melihat Korelasi antar Fitur, termasuk terhadap target)
# Ini membantu kita melihat variabel mana yang paling berhubungan dengan harga
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriks Korelasi (termasuk harga_rumah)")
plt.show()

# 2. HISTOGRAM (Melihat Distribusi Target)
# Membantu kita tahu apakah harga rumah terpusat di satu nilai atau menyebar luas
sns.histplot(df['harga_rumah'], kde=True, color='purple')
plt.title("Distribusi Harga Rumah Median")
plt.show()

# 3. SCATTER PLOT (Melihat Hubungan Dua Variabel)
# Apakah ada hubungan antara pendapatan dan harga rumah?
sns.scatterplot(x='pendapatan', y='harga_rumah', data=df)
plt.title("Hubungan Pendapatan vs Harga Rumah")
plt.show()