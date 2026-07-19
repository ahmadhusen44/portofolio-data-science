import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# 1. Load Data
df = pd.read_csv('Mall_Customers.csv')

# 2. Cek kolom dataset
print("Kolom yang tersedia:", df.columns.tolist())
print(df.head())

# 3. Tentukan Fitur untuk Clustering
# Catatan: Clustering TIDAK PUNYA target/label (beda dengan proyek California
# housing & iris sebelumnya yang supervised learning). Di sini kita cuma kasih
# fitur, lalu model sendiri yang menemukan pengelompokan alami dari data.
# Sekarang pakai 3 fitur (bukan cuma 2), supaya PCA nanti benar-benar berguna
# untuk meringkas dimensi menjadi 2D saat visualisasi.
fitur = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
X = df[fitur]

# 4. Standardisasi Fitur
# WAJIB untuk K-Means, karena K-Means menghitung jarak antar titik data.
# Kalau skala fitur beda jauh (misal umur 18-70 vs income 15-140), fitur
# dengan angka lebih besar akan mendominasi perhitungan jarak secara tidak adil.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Cari Jumlah Cluster (K) Optimal
# Karena tidak ada label, kita pakai 2 teknik untuk menentukan K terbaik:

# 5a. Elbow Method: plot inertia (total jarak kuadrat dalam cluster) vs K
# Cari titik "siku" di mana penurunan inertia mulai melandai
inertia = []
rentang_k = range(1, 11)
for k in rentang_k:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(rentang_k, inertia, marker='o')
plt.xlabel("Jumlah Cluster (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method untuk Menentukan K Optimal")
plt.xticks(rentang_k)
plt.show()

# 5b. Silhouette Score: mengukur kualitas pemisahan cluster (mendekati 1 = baik)
# Dimulai dari K=2 karena silhouette score butuh minimal 2 cluster
skor_silhouette = []
rentang_k_sil = range(2, 11)
for k in rentang_k_sil:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    label = kmeans.fit_predict(X_scaled)
    skor = silhouette_score(X_scaled, label)
    skor_silhouette.append(skor)
    print(f"K={k}: Silhouette Score = {skor:.4f}")

plt.figure(figsize=(8, 5))
plt.plot(rentang_k_sil, skor_silhouette, marker='o', color='green')
plt.xlabel("Jumlah Cluster (K)")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score untuk Menentukan K Optimal")
plt.xticks(rentang_k_sil)
plt.show()

# 6. Fit K-Means dengan K Terpilih
# TODO: Lihat grafik elbow & silhouette di atas, lalu ganti nilai K di bawah
# ini sesuai hasil analisis kamu. Untuk dataset ini, K=5 biasanya jadi pilihan
# umum, tapi cek dulu grafiknya, jangan langsung percaya angka ini.
k_optimal = 5
kmeans_final = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
df['cluster'] = kmeans_final.fit_predict(X_scaled)

print(f"\nJumlah pelanggan per cluster:")
print(df['cluster'].value_counts().sort_index())

# 7. PCA untuk Visualisasi
# Data clustering kita sekarang 3 dimensi (Age, Income, Spending Score), yang
# tidak bisa langsung digambar di grafik 2D biasa. PCA meringkas 3 dimensi itu
# menjadi 2 "komponen utama" yang menangkap variasi data sebanyak mungkin,
# supaya bisa divisualisasikan tanpa kehilangan terlalu banyak informasi.
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df['pca1'] = X_pca[:, 0]
df['pca2'] = X_pca[:, 1]

# Cek berapa persen variasi data yang berhasil ditangkap oleh 2 komponen ini.
# Semakin mendekati 100%, semakin sedikit informasi yang "hilang" saat diringkas.
variansi_terjelaskan = pca.explained_variance_ratio_
print(f"\nVariansi yang dijelaskan PC1: {variansi_terjelaskan[0]*100:.1f}%")
print(f"Variansi yang dijelaskan PC2: {variansi_terjelaskan[1]*100:.1f}%")
print(f"Total variansi terjelaskan (PC1+PC2): {sum(variansi_terjelaskan)*100:.1f}%")

# Loading: seberapa besar kontribusi tiap fitur ASLI terhadap PC1 dan PC2.
# Ini membantu menjawab "PC1 dan PC2 itu sebenarnya representasi dari apa?"
# Nilai mendekati +1 atau -1 = kontribusi besar; mendekati 0 = kontribusi kecil.
# Tanda (+/-) menunjukkan arah hubungan, bukan besar-kecilnya kontribusi.
loading = pd.DataFrame(
    pca.components_.T,
    columns=['PC1', 'PC2'],
    index=fitur
)
print("\nKontribusi tiap fitur terhadap PC1 & PC2:")
print(loading)

# Visualisasi loading dalam bentuk bar chart, lebih mudah dibaca daripada tabel
loading.plot(kind='bar', figsize=(8, 5))
plt.title("Kontribusi Fitur Asli terhadap PC1 & PC2")
plt.ylabel("Nilai Loading")
plt.axhline(0, color='black', linewidth=0.8)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Visualisasi Hasil Cluster di Ruang PCA (2D)
plt.figure(figsize=(9, 7))
sns.scatterplot(
    data=df, x='pca1', y='pca2',
    hue='cluster', palette='tab10', s=80
)
plt.xlabel(f"PC1 ({variansi_terjelaskan[0]*100:.1f}% variansi)")
plt.ylabel(f"PC2 ({variansi_terjelaskan[1]*100:.1f}% variansi)")
plt.title(f"Segmentasi Pelanggan Mall - Visualisasi PCA (K={k_optimal})")
plt.show()

# 8. Interpretasi Bisnis per Cluster
# Lihat rata-rata karakteristik tiap cluster untuk kasih nama/deskripsi bisnis
ringkasan_cluster = df.groupby('cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
print("\nRata-rata karakteristik per cluster:")
print(ringkasan_cluster)

# TODO: Setelah lihat ringkasan_cluster di atas, beri nama/interpretasi bisnis
# untuk tiap cluster. Contoh pola yang umum ditemukan di dataset ini:
# - Income tinggi, spending tinggi   -> "Pelanggan premium/target utama"
# - Income tinggi, spending rendah   -> "Income tinggi tapi hemat/selektif"
# - Income rendah, spending tinggi   -> "Impulsif, sensitif promo"
# - Income rendah, spending rendah   -> "Hemat, prioritas kebutuhan pokok"
# - Income & spending menengah       -> "Pelanggan rata-rata/standar"