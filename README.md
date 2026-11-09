# Analisis Ulasan Pelanggan Starbucks Menggunakan MapReduce

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi analisis data ulasan pelanggan Starbucks menggunakan Python dengan pendekatan algoritma MapReduce.

Tujuan proyek adalah menganalisis ulasan pelanggan untuk mengetahui pola kata yang sering muncul, distribusi rating, tren ulasan berdasarkan waktu, pembahasan produk, kualitas pelayanan, serta persebaran ulasan berdasarkan lokasi.

Hasil pengolahan data kemudian digunakan untuk menghasilkan business insights berupa temuan dan rekomendasi berdasarkan karakteristik ulasan pelanggan.

Seluruh hasil analisis disajikan melalui dashboard interaktif menggunakan Streamlit.

## 2. Tujuan Proyek

1. Memahami kualitas dan karakteristik dataset ulasan Starbucks.
2. Melakukan preprocessing terhadap teks ulasan.
3. Mengimplementasikan algoritma MapReduce untuk menghitung frekuensi kata.
4. Menganalisis distribusi dan kelompok rating pelanggan.
5. Menganalisis tren ulasan berdasarkan waktu.
6. Mengidentifikasi pembahasan produk dan kualitas pelayanan berdasarkan ulasan pelanggan.
7. Menganalisis persebaran ulasan berdasarkan lokasi Starbucks.
8. Menghasilkan business insights dan rekomendasi berdasarkan hasil analisis.

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

## 5. Metode dan Analisis

### A. Data Quality

Melakukan pemeriksaan kualitas dataset, meliputi:

- Missing values.
- Data duplikat.
- Rating tidak valid.
- Tanggal tidak valid.
- Jumlah lokasi unik.

### B. Text Preprocessing

Tahapan preprocessing teks ulasan:

- Mengubah teks menjadi huruf kecil.
- Menangani contraction.
- Menghapus URL.
- Menghapus karakter yang tidak diperlukan.
- Tokenisasi.
- Menghapus stopwords.
- Mempertahankan kata negasi seperti "not" dan "no".

### C. MapReduce

MapReduce digunakan untuk menghitung frekuensi kemunculan kata dalam ulasan pelanggan.

Tahapan proses:

1. **Mapper:** Memecah teks menjadi pasangan kata dan nilai 1.
2. **Shuffle:** Mengelompokkan nilai berdasarkan kata yang sama.
3. **Reducer:** Menjumlahkan seluruh frekuensi kemunculan setiap kata.

Analisis dilakukan pada seluruh ulasan dan berdasarkan kelompok rating:

- Low: rating 1–2.
- Medium: rating 3.
- High: rating 4–5.

Implementasi MapReduce dalam proyek ini menggunakan Python pada satu mesin, bukan cluster Hadoop atau Spark.

### D. Rating Analysis

Menganalisis karakteristik rating pelanggan, meliputi:

- Distribusi rating 1 sampai 5.
- Rata-rata rating.
- Median rating.
- Pengelompokan rating menjadi Low, Medium, dan High.
- Persentase masing-masing kelompok rating.

### E. Temporal Analysis

Menganalisis pola ulasan berdasarkan waktu, meliputi:

- Jumlah ulasan per tahun.
- Rata-rata rating per tahun.
- Jumlah ulasan per bulan.

### F. Product Analysis

Menganalisis pembahasan produk berdasarkan kata-kata yang muncul dalam ulasan pelanggan.

Analisis ini digunakan untuk mengetahui istilah produk yang paling sering dibicarakan oleh pelanggan.

### G. Service Analysis

Menganalisis pembahasan terkait kualitas pelayanan berdasarkan kata-kata dalam ulasan pelanggan.

Analisis ini digunakan untuk mengidentifikasi istilah pelayanan yang paling sering muncul dalam ulasan.

### H. Location Analysis

Menganalisis persebaran ulasan berdasarkan lokasi Starbucks.

Analisis ini digunakan untuk mengetahui lokasi dengan jumlah ulasan terbanyak sehingga dapat memberikan gambaran mengenai distribusi ulasan pelanggan berdasarkan lokasi.

### I. Business Insights

Menghasilkan temuan dan rekomendasi bisnis berdasarkan hasil pengolahan dan penggabungan beberapa analisis.

Business insights mencakup empat aspek utama:

1. **Customer Satisfaction:** Menggambarkan tingkat kepuasan pelanggan berdasarkan distribusi dan kelompok rating.
2. **Product Discussion:** Mengidentifikasi istilah produk yang paling sering dibicarakan pelanggan.
3. **Service Quality:** Mengidentifikasi istilah terkait pelayanan yang paling sering muncul dalam ulasan.
4. **Location Analysis:** Mengidentifikasi lokasi Starbucks dengan jumlah ulasan terbanyak.

Hasil business insights digunakan untuk memberikan gambaran mengenai karakteristik ulasan pelanggan serta mendukung pemahaman terhadap aspek produk, pelayanan, kepuasan, dan lokasi.

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
│   ├── product_analysis.py
│   ├── service_analysis.py
│   ├── location_analysis.py
│   ├── business_insight.py
│   └── visualization.py
│
├── results/
│
└── tests/
    └── test_mapreduce.py
```

## 7. Cara Menjalankan Proyek

### A. Clone Repository

```bash
git clone https://github.com/dzakkifm/analisis-starbucks-mapreduce.git
```

Masuk ke folder proyek:

```bash
cd analisis-starbucks-mapreduce
```

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

Pengujian dilakukan menggunakan Pytest untuk memastikan fungsi utama MapReduce berjalan sesuai dengan yang diharapkan.

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
3. Frekuensi kata tidak secara langsung menunjukkan sentimen atau penyebab ketidakpuasan pelanggan.
4. Data waktu memiliki rentang yang panjang sehingga pola temporal dapat dipengaruhi oleh proses pengumpulan dataset.
5. Analisis produk dan pelayanan bergantung pada istilah yang ditemukan dalam teks ulasan.
6. Analisis lokasi menggambarkan jumlah ulasan dalam dataset, bukan secara langsung menunjukkan kualitas seluruh gerai Starbucks.
7. Implementasi MapReduce menggunakan Python secara lokal dan bukan sistem komputasi terdistribusi.

## 10. Kesimpulan

Proyek ini menerapkan algoritma MapReduce untuk mengolah dan menganalisis frekuensi kata dalam ulasan pelanggan Starbucks. Hasilnya dikombinasikan dengan analisis rating, temporal, produk, pelayanan, dan lokasi untuk memperoleh gambaran yang lebih luas mengenai karakteristik ulasan pelanggan.

Melalui fitur Business Insights, hasil analisis diolah menjadi informasi mengenai kepuasan pelanggan, pembahasan produk, kualitas pelayanan, dan lokasi dengan jumlah ulasan terbanyak.

Dashboard interaktif berbasis Streamlit digunakan untuk menyajikan hasil pengolahan data sehingga informasi dapat dipahami dengan lebih mudah dan dapat menjadi bahan pertimbangan dalam memahami pengalaman pelanggan.

---

**Big Data Analytics Project**

Python | MapReduce | Streamlit | Pandas | Plotly