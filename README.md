
# Analisis Ulasan Pelanggan Starbucks Menggunakan MapReduce

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi analisis data ulasan pelanggan Starbucks menggunakan Python dan algoritma MapReduce.

Tujuan proyek adalah menganalisis ulasan pelanggan untuk mengetahui pola kata yang sering muncul, distribusi rating, tren ulasan berdasarkan waktu, serta menghasilkan insight dan rekomendasi bisnis.

Hasil analisis ditampilkan melalui dashboard interaktif menggunakan Streamlit.

## 2. Tujuan Proyek

1. Memahami kualitas dan karakteristik dataset ulasan Starbucks.
2. Melakukan preprocessing terhadap teks ulasan.
3. Mengimplementasikan algoritma MapReduce untuk menghitung frekuensi kata.
4. Menganalisis distribusi rating pelanggan.
5. Menganalisis tren ulasan berdasarkan waktu.
6. Menghasilkan insight dan rekomendasi berdasarkan hasil analisis.

## 3. Dataset

Dataset yang digunakan adalah `reviews_data.csv`.

Dataset memiliki 850 baris dan 6 kolom utama:

| Kolom | Keterangan |
|---|---|
| name | Nama reviewer |
| location | Lokasi Starbucks |
| date | Tanggal ulasan |
| rating | Rating pelanggan |
| review | Isi ulasan |
| image_links | Informasi tautan gambar |

Tanggal ulasan yang valid mencakup periode 19 Juli 2000 sampai 14 September 2023.

Terdapat 705 rating valid dan 145 rating kosong.

## 4. Teknologi yang Digunakan

- Python 3.12
- Pandas
- NumPy
- Streamlit
- Plotly
- Matplotlib
- WordCloud
- Pytest

## 5. Metode Analisis

### A. Data Quality

Melakukan pemeriksaan:
- Missing values.
- Data duplikat.
- Rating tidak valid.
- Tanggal tidak valid.
- Jumlah lokasi unik.

### B. Text Preprocessing

Tahapan preprocessing:
- Mengubah teks menjadi huruf kecil.
- Menangani contraction.
- Menghapus URL.
- Menghapus karakter yang tidak diperlukan.
- Tokenisasi.
- Menghapus stopwords.
- Mempertahankan kata negasi seperti "not" dan "no".

### C. MapReduce

MapReduce digunakan untuk menghitung frekuensi kemunculan kata dalam ulasan.

Tahapan:
1. Mapper: memecah teks menjadi pasangan kata dan nilai 1.
2. Shuffle: mengelompokkan nilai berdasarkan kata.
3. Reducer: menjumlahkan frekuensi setiap kata.

Analisis dilakukan pada seluruh ulasan dan berdasarkan kelompok rating:
- Low: rating 1–2.
- Medium: rating 3.
- High: rating 4–5.

Implementasi MapReduce dalam proyek ini menggunakan Python pada satu mesin, bukan cluster Hadoop atau Spark.

### D. Rating Analysis

Menganalisis:
- Distribusi rating 1 sampai 5.
- Rata-rata rating.
- Median rating.
- Kelompok rating rendah, sedang, dan tinggi.

### E. Temporal Analysis

Menganalisis:
- Jumlah ulasan per tahun.
- Rata-rata rating per tahun.
- Jumlah ulasan per bulan.

### F. Business Insight

Menghasilkan temuan dan rekomendasi berdasarkan hasil analisis rating dan frekuensi kata.

## 6. Struktur Folder

```text
analisis-starbucks-mapreduce/
│
├── app.py
├── requirements.txt
├── pytest.ini
├── README.md
│
├── data/
│   └── reviews_data.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_quality.py
│   ├── preprocessing.py
│   ├── mapper.py
│   ├── shuffle.py
│   ├── reducer.py
│   ├── mapreduce.py
│   ├── rating_analysis.py
│   ├── temporal_analysis.py
│   ├── business_insight.py
│   └── visualization.py
│
├── results/
│
└── tests/
    └── test_mapreduce.py
```

## 7. Cara Menjalankan Proyek

### A. Clone atau Download Proyek

Buka folder proyek melalui VS Code.

### B. Membuat Virtual Environment

```bash
python -m venv .venv
```

Aktifkan virtual environment pada Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### C. Install Dependencies

```bash
pip install -r requirements.txt
```

### D. Menjalankan Dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka melalui browser.

### E. Menjalankan Pengujian

```bash
pytest -v
```

## 8. Hasil Pengujian

Pengujian dilakukan menggunakan Pytest.

Hasil pengujian terakhir:

```text
6 passed in 0.06s
```

Enam pengujian meliputi:
- Mapper.
- Mapper untuk teks kosong.
- Shuffle.
- Reducer.
- Integrasi MapReduce.
- Fungsi Top Words.

## 9. Batasan Analisis

1. Dataset memiliki 850 ulasan dan tidak dapat dianggap mewakili seluruh pelanggan Starbucks.
2. Sebanyak 145 ulasan tidak memiliki rating.
3. Frekuensi kata tidak secara langsung menunjukkan sentimen atau penyebab ketidakpuasan.
4. Data waktu memiliki rentang yang panjang sehingga pola temporal dapat dipengaruhi oleh proses pengumpulan dataset.
5. Implementasi MapReduce menggunakan Python secara lokal dan bukan sistem komputasi terdistribusi.

## 10. Kesimpulan

Proyek ini menerapkan MapReduce untuk menganalisis frekuensi kata dalam ulasan pelanggan Starbucks. Analisis tersebut dikombinasikan dengan analisis rating dan temporal untuk memperoleh gambaran mengenai pola ulasan pelanggan.

Dashboard Streamlit digunakan untuk menyajikan hasil analisis secara interaktif sehingga informasi dapat dipahami dengan lebih mudah.

---

**Big Data Analytics Project**

Python | MapReduce | Streamlit | Pandas | Plotly
