-- Kumpulan Query Analitis: Segmentasi Pelanggan Mall
-- Jalankan setelah etl_pipeline.py berhasil mengisi database

USE db_mall_customers;

-- ============================================
-- 1. JOIN DASAR
-- Gabungkan data demografis & perilaku belanja
-- ============================================
SELECT
    p.customer_id,
    p.gender,
    p.age,
    pb.annual_income_kusd,
    pb.spending_score
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
ORDER BY p.customer_id
LIMIT 10;


-- ============================================
-- 2. GROUP BY & AGGREGATION
-- Rata-rata spending score per gender
-- ============================================
SELECT
    p.gender,
    COUNT(*) AS jumlah_pelanggan,
    ROUND(AVG(pb.spending_score), 2) AS rata_rata_spending,
    ROUND(AVG(pb.annual_income_kusd), 2) AS rata_rata_income
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
GROUP BY p.gender;


-- ============================================
-- 3. GROUP BY dengan kategori usia (CASE WHEN)
-- Segmentasi manual berdasarkan kelompok usia
-- ============================================
SELECT
    CASE
        WHEN p.age < 25 THEN '< 25 tahun'
        WHEN p.age BETWEEN 25 AND 40 THEN '25-40 tahun'
        WHEN p.age BETWEEN 41 AND 60 THEN '41-60 tahun'
        ELSE '> 60 tahun'
    END AS kelompok_usia,
    COUNT(*) AS jumlah_pelanggan,
    ROUND(AVG(pb.spending_score), 2) AS rata_rata_spending
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
GROUP BY kelompok_usia
ORDER BY kelompok_usia;


-- ============================================
-- 4. WINDOW FUNCTION: RANK()
-- Ranking pelanggan berdasarkan spending score PER GENDER
-- (beda dengan ORDER BY biasa -- ranking-nya dimulai ulang tiap kelompok gender)
-- ============================================
SELECT
    p.customer_id,
    p.gender,
    p.age,
    pb.spending_score,
    RANK() OVER (PARTITION BY p.gender ORDER BY pb.spending_score DESC) AS ranking_dalam_gender
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
ORDER BY p.gender, ranking_dalam_gender
LIMIT 20;


-- ============================================
-- 5. WINDOW FUNCTION: perbandingan dengan rata-rata keseluruhan
-- Selisih spending score tiap pelanggan terhadap rata-rata semua pelanggan
-- ============================================
SELECT
    p.customer_id,
    pb.spending_score,
    ROUND(AVG(pb.spending_score) OVER (), 2) AS rata_rata_keseluruhan,
    ROUND(pb.spending_score - AVG(pb.spending_score) OVER (), 2) AS selisih_dari_rata_rata
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
ORDER BY selisih_dari_rata_rata DESC
LIMIT 10;


-- ============================================
-- 6. CTE (Common Table Expression) dengan WITH
-- Cari pelanggan "premium": income tinggi (top 25%) DAN spending tinggi (top 25%)
-- ============================================
WITH batas_income AS (
    SELECT
        annual_income_kusd,
        NTILE(4) OVER (ORDER BY annual_income_kusd) AS kuartil_income
    FROM profil_belanja
),
batas_spending AS (
    SELECT
        customer_id,
        spending_score,
        NTILE(4) OVER (ORDER BY spending_score) AS kuartil_spending
    FROM profil_belanja
)
SELECT
    p.customer_id,
    p.gender,
    p.age,
    pb.annual_income_kusd,
    pb.spending_score
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
JOIN batas_spending bs ON p.customer_id = bs.customer_id
WHERE pb.annual_income_kusd >= (
        SELECT MIN(annual_income_kusd) FROM batas_income WHERE kuartil_income = 4
    )
    AND bs.kuartil_spending = 4
ORDER BY pb.annual_income_kusd DESC;


-- ============================================
-- 7. Subquery: pelanggan dengan spending score di atas rata-rata
-- ============================================
SELECT p.customer_id, p.gender, p.age, pb.spending_score
FROM pelanggan p
JOIN profil_belanja pb ON p.customer_id = pb.customer_id
WHERE pb.spending_score > (
    SELECT AVG(spending_score) FROM profil_belanja
)
ORDER BY pb.spending_score DESC;
