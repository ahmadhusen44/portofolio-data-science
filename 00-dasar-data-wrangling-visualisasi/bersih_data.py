import pandas as pd
import numpy as np

# Data Awal
data = {
    'Nama': ['Andi', 'Budi', 'Caca', 'Dedi', 'Euis', 'Fajar'],
    'Usia': [25, np.nan, 22, 30, np.nan, 28],
    'Gaji': [5000, 6000, np.nan, np.nan, np.nan, np.nan]
}

# 1. Analisis dengan cara Dropna (Menghapus data)
df_drop = pd.DataFrame(data)
df_drop = df_drop.dropna()
print("\n--- Hasil dengan Dropna (Menghapus Data) ---")
print(df_drop)

# 2. Analisis dengan cara Imputasi (Mengisi data)
df_impute = pd.DataFrame(data)
# Isi Usia dengan mean
df_impute['Usia'] = df_impute['Usia'].fillna(df_impute['Usia'].mean())
# Isi Gaji dengan mean
df_impute['Gaji'] = df_impute['Gaji'].fillna(df_impute['Gaji'].mean())

print("\n--- Hasil dengan Imputasi (Mengisi Data) ---")
print(df_impute)