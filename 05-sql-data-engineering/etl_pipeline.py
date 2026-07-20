"""
ETL Pipeline: Mall_Customers.csv -> MySQL Database

CARA MENJALANKAN:
1. Pastikan MySQL sudah jalan (XAMPP/Workbench) dan schema.sql sudah
   dijalankan dulu di MySQL untuk membuat database & tabelnya.
2. Sesuaikan KONFIGURASI_DB di bawah dengan kredensial MySQL kamu.
3. Install dependency: pip install mysql-connector-python pandas
4. Jalankan: python etl_pipeline.py
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error

# ==== KONFIGURASI DATABASE ====
# Sesuaikan dengan setup MySQL kamu (default XAMPP biasanya user=root, password kosong)
KONFIGURASI_DB = {
    "host": "localhost",
    "user": "root",
    "password": "",       # ganti sesuai password MySQL kamu
    "database": "db_mall_customers"
}


def extract(path_csv):
    """EXTRACT: baca data mentah dari CSV."""
    print("[EXTRACT] Membaca data dari", path_csv)
    df = pd.read_csv(path_csv)
    print(f"[EXTRACT] Berhasil, {len(df)} baris ditemukan.")
    return df


def transform(df):
    """TRANSFORM: bersihkan & pisahkan data jadi 2 tabel sesuai skema."""
    print("[TRANSFORM] Membersihkan & menstrukturkan data...")

    # Validasi dasar: hapus baris yang datanya tidak lengkap (kalau ada)
    sebelum = len(df)
    df = df.dropna()
    sesudah = len(df)
    if sebelum != sesudah:
        print(f"[TRANSFORM] Menghapus {sebelum - sesudah} baris dengan data kosong.")

    # Validasi tipe data & rentang nilai wajar
    df = df[(df["Age"] > 0) & (df["Age"] < 120)]
    df = df[(df["Spending Score (1-100)"] >= 0) & (df["Spending Score (1-100)"] <= 100)]

    # Pisahkan jadi 2 dataframe sesuai skema 2 tabel
    df_pelanggan = df[["CustomerID", "Gender", "Age"]].copy()
    df_profil = df[["CustomerID", "Annual Income (k$)", "Spending Score (1-100)"]].copy()
    df_profil = df_profil.rename(columns={"CustomerID": "customer_id"})

    print(f"[TRANSFORM] Selesai. {len(df_pelanggan)} baris siap di-load.")
    return df_pelanggan, df_profil


def load(df_pelanggan, df_profil, config):
    """LOAD: masukkan data yang sudah bersih ke MySQL."""
    print("[LOAD] Menghubungkan ke MySQL...")
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Kosongkan dulu tabel supaya bisa dijalankan berulang tanpa duplikat
        # (urutan penting: hapus profil_belanja dulu karena ada foreign key)
        cursor.execute("DELETE FROM profil_belanja")
        cursor.execute("DELETE FROM pelanggan")

        # Insert ke tabel pelanggan
        sql_pelanggan = """
            INSERT INTO pelanggan (customer_id, gender, age)
            VALUES (%s, %s, %s)
        """
        data_pelanggan = list(df_pelanggan.itertuples(index=False, name=None))
        cursor.executemany(sql_pelanggan, data_pelanggan)

        # Insert ke tabel profil_belanja
        sql_profil = """
            INSERT INTO profil_belanja (customer_id, annual_income_kusd, spending_score)
            VALUES (%s, %s, %s)
        """
        data_profil = list(df_profil.itertuples(index=False, name=None))
        cursor.executemany(sql_profil, data_profil)

        conn.commit()
        print(f"[LOAD] Berhasil! {cursor.rowcount} baris terakhir di-insert ke profil_belanja.")
        print(f"[LOAD] Total: {len(data_pelanggan)} baris ke tabel pelanggan, "
              f"{len(data_profil)} baris ke tabel profil_belanja.")

    except Error as e:
        print("[LOAD] Gagal terhubung/insert ke MySQL:", e)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("[LOAD] Koneksi MySQL ditutup.")


if __name__ == "__main__":
    df_mentah = extract("Mall_Customers.csv")
    df_pelanggan, df_profil = transform(df_mentah)
    load(df_pelanggan, df_profil, KONFIGURASI_DB)
    print("\n=== ETL Pipeline selesai ===")