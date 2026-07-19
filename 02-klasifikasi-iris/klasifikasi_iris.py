# ALGORITMA KLASIFIKASI IRIS VERSI FINAL
import tensorflow as tf
import numpy as np
import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=== ALGORITMA KLASIFIKASI BUNGA IRIS ===")

# C. PENJELASAN BARIS PER BARIS ADA DI KOMENTAR #

# LANGKAH 1: AMBIL DATA
iris = load_iris() # load_iris() = ambil dataset iris bawaan sklearn. Isinya 150 data
X = iris.data # X = fitur: [panjang kelopak, lebar kelopak, panjang mahkota, lebar mahkota]
y = iris.target # y = label: 0=setosa, 1=versicolor, 2=virginica
nama_bunga = iris.target_names
print(f"Data ada {len(X)} bunga")

# LANGKAH 2: BAGI DATA
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# test_size=0.2 artinya 20% buat tes, 80% buat latih

# B. LANGKAH SIMPAN & LOAD MODEL + SCALER
model_path = "model_iris.keras"  # format native Keras 3 (.h5 sudah deprecated)
scaler_path = "scaler_iris.pkl"  # scaler disimpan terpisah biar konsisten dengan model

if os.path.exists(model_path) and os.path.exists(scaler_path):
    # kalau model & scaler udah ada, langsung load dua-duanya
    # (scaler WAJIB ikut disimpan, karena scaler yang di-fit ulang dari split
    # data yang berbeda bisa menghasilkan skala berbeda dari saat training awal)
    print("\nModel & scaler sudah ada. Langsung load...")
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X_test = scaler.transform(X_test)
else:
    # LANGKAH 3: NORMALISASI (hanya saat training dari awal)
    scaler = StandardScaler()  # biar semua angka skalanya sama, biar model cepat belajar
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("\nModel belum ada. Melatih dari awal...")
    # BIKIN MODEL / OTAK
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(4,)), # Lapisan tersembunyi 1. 32 neuron
        tf.keras.layers.Dense(16, activation='relu'), # Lapisan tersembunyi 2. 16 neuron
        tf.keras.layers.Dense(3, activation='softmax') # Lapisan output. 3 karena ada 3 jenis bunga. softmax = buat probabilitas
    ])

    # KOMPILASI = setting cara belajarnya
    model.compile(optimizer='adam', # adam = algoritma buat ngatur biar cepat pinter
                  loss='sparse_categorical_crossentropy', # rumus buat ngukur salahnya
                  metrics=['accuracy']) # metrik yang kita lihat = akurasi

    # LATIH MODEL
    print("Sedang melatih otak komputer...")
    model.fit(X_train, y_train, epochs=100, verbose=1) # epochs=100 = diulang belajar 100x
    print("Selesai dilatih!")

    # SIMPAN MODEL & SCALER BIAR GAK LATIH ULANG
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model disimpan ke {model_path}")
    print(f"Scaler disimpan ke {scaler_path}")

# UJI AKURASI
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nAkurasi Model: {accuracy * 100:.2f}%")

# A. LANGKAH INPUT SENDIRI DARI KEYBOARD
print("\n--- COBA PREDIKSI SENDIRI ---")
print("Masukkan ukuran bunga. Pisahkan dengan koma")
print("Urutan: Panjang Kelopak, Lebar Kelopak, Panjang Mahkota, Lebar Mahkota")

try:
    input_user = input("Contoh: 5.1,3.5,1.4,0.2 \nInput: ")
    ukuran = [float(x) for x in input_user.split(',')] # ubah "5.1,3.5" jadi [5.1, 3.5]
    ukuran = np.array([ukuran]) # ubah jadi format yang dimengerti tensorflow

    ukuran = scaler.transform(ukuran) # wajib di normalisasi juga
    prediksi = model.predict(ukuran, verbose=0)

    jenis = nama_bunga[prediksi.argmax()] # argmax = ambil index probabilitas tertinggi
    probabilitas = np.max(prediksi) * 100

    print(f"\nHasil Prediksi: {jenis}")
    print(f"Tingkat Keyakinan: {probabilitas:.2f}%")

except ValueError:
    print("Format salah. Harus 4 angka dipisah koma")