import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat dataset (Jika Anda sudah download csv-nya, gunakan pd.read_csv('iris.csv'))
# Untuk latihan cepat, Seaborn punya dataset bawaan
df = sns.load_dataset('iris')

print("--- 5 Baris Pertama Data Iris ---")
print(df.head())

# 1. Scatterplot: Melihat hubungan antara dua variabel (panjang & lebar kelopak)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='sepal_length', y='sepal_width', hue='species', style='species', s=100)
plt.title('Hubungan Panjang dan Lebar Sepal berdasarkan Spesies')
plt.show()

# 2. Pairplot: Melihat hubungan semua variabel sekaligus (Sangat berguna untuk AI Engineer!)
# Ini adalah cara cepat untuk melihat pola data sebelum membuat model
sns.pairplot(df, hue='species')
plt.show()

# 3. Boxplot: Melihat sebaran data dan outliers
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='species', y='petal_length')
plt.title('Sebaran Panjang Petal per Spesies')
plt.show()