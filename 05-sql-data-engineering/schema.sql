-- Skema Database: Segmentasi Pelanggan Mall
-- Sengaja dipecah jadi 2 tabel (bukan 1 tabel flat seperti CSV aslinya)
-- untuk latihan normalisasi dan JOIN antar tabel.

CREATE DATABASE IF NOT EXISTS db_mall_customers;
USE db_mall_customers;

-- Tabel 1: data demografis pelanggan
CREATE TABLE IF NOT EXISTS pelanggan (
    customer_id INT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL
);

-- Tabel 2: data perilaku belanja pelanggan
-- Dipisah dari tabel pelanggan karena secara konsep ini "kategori data" yang
-- berbeda (demografi vs perilaku) -- pemisahan seperti ini yang jadi dasar
-- desain database yang baik, walau di kasus nyata datanya tetap 1-ke-1.
CREATE TABLE IF NOT EXISTS profil_belanja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    annual_income_kusd DECIMAL(10,2) NOT NULL,
    spending_score INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES pelanggan(customer_id)
);

-- Index tambahan untuk mempercepat query yang sering filter/join by customer_id
CREATE INDEX idx_profil_customer ON profil_belanja(customer_id);
