
import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.preprocessing import preprocess_dataset
from src.mapreduce import run_mapreduce, get_top_words, run_mapreduce_by_rating
from src.rating_analysis import analyze_ratings
from src.temporal_analysis import analyze_temporal
from src.product_analysis import analyze_products
from src.service_analysis import analyze_service
from src.location_analysis import analyze_locations
from src.business_insight import generate_business_insights
from src.visualization import (
    plot_rating_distribution,
    plot_yearly_reviews,
    plot_yearly_rating,
    plot_monthly_reviews
)
import inspect

print("LOKASI FUNGSI:", inspect.getfile(generate_business_insights))
print("PARAMETER FUNGSI:", inspect.signature(generate_business_insights))

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Analisis Starbucks Reviews",
    page_icon="☕",
    layout="wide"
)


# ==========================================
# LOAD DAN PREPROCESS DATA
# ==========================================

@st.cache_data
def load_processed_data():
    data = load_dataset()
    data = preprocess_dataset(data)
    return data


data = load_processed_data()

# Hasil analisis utama
rating_result = analyze_ratings(data)
temporal_result = analyze_temporal(data)


# ==========================================
# SIDEBAR NAVIGASI
# ==========================================

st.sidebar.title("☕ Starbucks Analytics")

menu = st.sidebar.radio(
    "Pilih Menu:",
    [
        "Overview",
        "MapReduce",
        "Rating Analysis",
        "Product Discussion Analysis",
        "Service Quality Analysis",
        "Location Analysis",
        "Temporal Analysis",
        "Business Insight"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Dashboard analisis ulasan pelanggan Starbucks "
    "menggunakan Python dan algoritma MapReduce."
)


# ==========================================
# JUDUL DASHBOARD
# ==========================================

st.title("☕ Analisis Ulasan Pelanggan Starbucks")

st.caption(
    "Analisis Data Ulasan Pelanggan Menggunakan MapReduce dan Python"
)


# ==========================================
# MENU 1: OVERVIEW
# ==========================================

if menu == "Overview":

    st.header("Overview Dataset")

    total_reviews = len(data)
    valid_rating = data["rating"].notna().sum()
    average_rating = data["rating"].mean()
    unique_locations = data["location"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Ulasan",
        f"{total_reviews:,}"
    )

    col2.metric(
        "Rating Valid",
        f"{valid_rating:,}"
    )

    col3.metric(
        "Rata-rata Rating",
        f"{average_rating:.2f} / 5"
    )

    col4.metric(
        "Lokasi Unik",
        f"{unique_locations:,}"
    )

    st.divider()

    st.subheader("Preview Dataset")

    st.dataframe(
        data.head(10),
        use_container_width=True
    )

    st.subheader("Informasi Dataset")

    st.write(
        "Dataset berisi ulasan pelanggan Starbucks "
        "yang digunakan untuk menganalisis rating, "
        "frekuensi kata, dan tren ulasan."
    )

    st.write("Jumlah baris:", total_reviews)
    st.write("Jumlah kolom:", len(data.columns))
    st.write("Jumlah rating kosong:", data["rating"].isna().sum())
    st.write("Jumlah review kosong:", data["review"].isna().sum())


# ==========================================
# MENU 2: MAPREDUCE
# ==========================================

elif menu == "MapReduce":

    st.header("Analisis Frekuensi Kata dengan MapReduce")

    st.write(
        "Proses MapReduce digunakan untuk menghitung "
        "frekuensi kemunculan kata dalam ulasan pelanggan."
    )

    # --------------------------------------
    # MAPREDUCE KESELURUHAN
    # --------------------------------------

    st.subheader("Frekuensi Kata Keseluruhan")

    texts = data["review_clean"].dropna()
    texts = texts[texts.str.strip() != ""]

    word_counts = run_mapreduce(texts)

    top_words = get_top_words(word_counts, 20)

    word_df = pd.DataFrame(
        top_words,
        columns=["Kata", "Frekuensi"]
    )

    st.dataframe(
        word_df,
        use_container_width=True
    )

    st.bar_chart(
        word_df.set_index("Kata")
    )

    st.divider()

    # --------------------------------------
    # MAPREDUCE BERDASARKAN RATING
    # --------------------------------------

    st.subheader("Frekuensi Kata Berdasarkan Kelompok Rating")

    rating_groups = {
        "low": "Rating Rendah (1–2)",
        "medium": "Rating Sedang (3)",
        "high": "Rating Tinggi (4–5)"
    }

    for group, label in rating_groups.items():

        st.markdown(f"### {label}")

        group_data = data[
            data["rating_group"] == group
        ]

        group_texts = group_data["review_clean"].dropna()
        group_texts = group_texts[
            group_texts.str.strip() != ""
        ]

        group_word_counts = run_mapreduce(group_texts)

        group_top_words = get_top_words(
            group_word_counts,
            10
        )

        group_df = pd.DataFrame(
            group_top_words,
            columns=["Kata", "Frekuensi"]
        )

        st.write(
            f"Jumlah ulasan: {len(group_data):,}"
        )

        st.dataframe(
            group_df,
            use_container_width=True
        )


# ==========================================
# MENU 3: RATING ANALYSIS
# ==========================================

elif menu == "Rating Analysis":

    st.header("Analisis Rating Pelanggan")

    st.write(
        "Analisis ini digunakan untuk mengetahui "
        "distribusi rating dan gambaran kepuasan pelanggan."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rating Valid",
        f"{rating_result['total_reviews']:,}"
    )

    col2.metric(
        "Rata-rata Rating",
        f"{rating_result['average_rating']:.2f} / 5"
    )

    col3.metric(
        "Median Rating",
        f"{rating_result['median_rating']:.2f}"
    )

    st.divider()

    # --------------------------------------
    # DISTRIBUSI RATING
    # --------------------------------------

    st.subheader("Distribusi Rating")

    rating_counts = rating_result["rating_counts"]

    rating_chart = plot_rating_distribution(
        rating_counts
    )

    st.plotly_chart(
        rating_chart,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------
    # KELOMPOK RATING
    # --------------------------------------

    st.subheader("Kelompok Rating")

    group_counts = rating_result["group_counts"]
    group_percentages = rating_result["group_percentages"]

    group_df = pd.DataFrame({
        "Kelompok": ["LOW", "MEDIUM", "HIGH"],
        "Jumlah Ulasan": [
            group_counts["low"],
            group_counts["medium"],
            group_counts["high"]
        ],
    "Persentase (%)": [
        group_percentages["low"],
        group_percentages["medium"],
        group_percentages["high"]
    ]
})

    st.dataframe(
        group_df,
        use_container_width=True
    )

    st.caption(
        "Persentase dihitung berdasarkan 705 rating valid. "
        "Ulasan tanpa rating tidak dimasukkan dalam perhitungan."
    )



elif menu == "Product Discussion Analysis":

    st.header("Product Discussion Analysis")

    st.write(
        "Analisis istilah produk dan minuman Starbucks "
        "yang paling sering disebut pelanggan dalam ulasan "
        "menggunakan algoritma MapReduce."
    )

    # Menjalankan analisis produk
    product_result = analyze_products(data, top_n=10)

    # Metrik utama
    col1, col2 = st.columns(2)

    col1.metric(
        "Jumlah Ulasan Diproses",
        f"{product_result['total_reviews']:,}"
    )

    col2.metric(
        "Total Penyebutan Istilah Produk",
        f"{product_result['total_product_mentions']:,}"
    )

    st.divider()

    # Top 10 produk
    st.subheader("Top 10 Istilah Produk yang Disebut")

    product_df = pd.DataFrame(
        product_result["top_products"],
        columns=["Istilah Produk", "Frekuensi"]
    )

    if not product_df.empty:

        st.dataframe(
            product_df,
            use_container_width=True
        )

        st.bar_chart(
            product_df.set_index("Istilah Produk")
        )

    else:
        st.info("Belum ditemukan istilah produk dalam ulasan.")

    st.divider()

    # Perbandingan berdasarkan rating
    st.subheader("Perbandingan Penyebutan Produk Berdasarkan Rating")

    group_labels = {
        "low": "Rating Rendah (1–2)",
        "medium": "Rating Sedang (3)",
        "high": "Rating Tinggi (4–5)"
    }

    for group, label in group_labels.items():

        st.markdown(f"### {label}")

        group_products = product_result[
            "product_by_rating"
        ][group]

        group_df = pd.DataFrame(
            group_products,
            columns=["Istilah Produk", "Frekuensi"]
        )

        if not group_df.empty:

            st.dataframe(
                group_df,
                use_container_width=True
            )

            st.bar_chart(
                group_df.set_index("Istilah Produk")
            )

        else:
            st.info("Tidak ditemukan istilah produk.")

    st.divider()

    st.subheader("Kesimpulan Analisis")

    if not product_df.empty:

        most_mentioned = product_df.iloc[0]

        st.write(
            f"Istilah produk yang paling sering disebut adalah "
            f"**{most_mentioned['Istilah Produk']}**, "
            f"dengan frekuensi {most_mentioned['Frekuensi']} kali."
        )

    st.caption(
        "Catatan: Hasil menunjukkan frekuensi penyebutan istilah "
        "produk dalam ulasan, bukan jumlah produk yang terjual. "
        "Daftar istilah produk menggunakan pencocokan kata yang "
        "telah ditentukan sebelumnya."
    )



elif menu == "Service Quality Analysis":
    st.title("Service Quality Analysis")
    st.write(
        "Analisis istilah yang berkaitan dengan kualitas "
        "pelayanan berdasarkan ulasan pelanggan Starbucks."
    )

    service_result = analyze_service(data, top_n=10)

    col1, col2 = st.columns(2)

    col1.metric(
        "Jumlah Ulasan Diproses",
        f"{service_result['total_reviews']:,}"
    )

    col2.metric(
        "Total Penyebutan Istilah Pelayanan",
        f"{service_result['total_service_mentions']:,}"
    )

    st.subheader("Top 10 Istilah Pelayanan")

    service_df = pd.DataFrame(
        service_result["top_service_words"],
        columns=["Istilah Pelayanan", "Frekuensi"]
    )

    if not service_df.empty:
        st.dataframe(service_df, use_container_width=True)
        st.bar_chart(
            service_df.set_index("Istilah Pelayanan")
        )
    else:
        st.info("Tidak ditemukan istilah pelayanan.")

    st.subheader("Perbandingan Istilah Berdasarkan Rating")

    for group in ["low", "medium", "high"]:
        st.markdown(f"### Rating {group.upper()}")

        group_df = pd.DataFrame(
            service_result["service_by_rating"][group],
            columns=["Istilah Pelayanan", "Frekuensi"]
        )

        if not group_df.empty:
            st.dataframe(group_df, use_container_width=True)
            st.bar_chart(
                group_df.set_index("Istilah Pelayanan")
            )
        else:
            st.info("Tidak ada istilah yang ditemukan.")

    st.caption(
        "Catatan: Frekuensi menunjukkan jumlah kemunculan kata "
        "dalam ulasan, bukan penilaian otomatis terhadap kualitas "
        "pelayanan. Analisis menggunakan daftar kata kunci."
    )


elif menu == "Location Analysis":
    st.title("Location Analysis")

    st.write(
        "Analisis persebaran ulasan dan rata-rata rating "
        "berdasarkan lokasi Starbucks."
    )

    location_result = analyze_locations(data, top_n=10)

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Lokasi",
        f"{location_result['total_locations']:,}"
    )

    col2.metric(
        "Total Ulasan",
        f"{location_result['total_reviews']:,}"
    )

    # Top lokasi berdasarkan jumlah ulasan
    st.subheader("Top 10 Lokasi Berdasarkan Jumlah Ulasan")

    location_df = location_result["top_locations"].copy()

    location_df = location_df.rename(columns={
        "location": "Lokasi",
        "total_reviews": "Jumlah Ulasan",
        "average_rating": "Rata-rata Rating",
        "rated_reviews": "Ulasan dengan Rating"
    })

    location_df["Rata-rata Rating"] = (
        location_df["Rata-rata Rating"].round(2)
    )

    st.dataframe(
        location_df,
        use_container_width=True
    )

    chart_data = location_result["top_locations"].set_index(
        "location"
    )["total_reviews"]

    st.bar_chart(chart_data)

    # Top lokasi berdasarkan rata-rata rating
    st.subheader("Top 10 Lokasi Berdasarkan Rata-rata Rating")

    rated_df = location_result["top_rated_locations"].copy()

    rated_df = rated_df.rename(columns={
        "location": "Lokasi",
        "total_reviews": "Jumlah Ulasan",
        "average_rating": "Rata-rata Rating",
        "rated_reviews": "Ulasan dengan Rating"
    })

    rated_df["Rata-rata Rating"] = (
        rated_df["Rata-rata Rating"].round(2)
    )

    st.dataframe(
        rated_df,
        use_container_width=True
    )

    st.caption(
        "Catatan: Rata-rata rating hanya dihitung dari ulasan "
        "yang memiliki rating. Lokasi dengan jumlah ulasan "
        "sedikit dapat memiliki rata-rata rating yang kurang "
        "representatif."
    )


# ==========================================
# MENU 4: TEMPORAL ANALYSIS
# ==========================================

elif menu == "Temporal Analysis":

    st.header("Analisis Tren Ulasan Berdasarkan Waktu")

    st.write(
        "Analisis temporal digunakan untuk mengetahui "
        "perubahan jumlah ulasan dan rata-rata rating "
        "berdasarkan waktu."
    )

    yearly_reviews, yearly_rating, monthly_reviews = temporal_result

    # --------------------------------------
    # ULASAN PER TAHUN
    # --------------------------------------

    st.subheader("Jumlah Ulasan per Tahun")

    yearly_reviews_chart = plot_yearly_reviews(
        yearly_reviews
    )

    st.plotly_chart(
        yearly_reviews_chart,
        use_container_width=True
    )

    st.dataframe(
        yearly_reviews,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------
    # RATING PER TAHUN
    # --------------------------------------

    st.subheader("Rata-rata Rating per Tahun")

    yearly_rating_chart = plot_yearly_rating(
        yearly_rating
    )

    st.plotly_chart(
        yearly_rating_chart,
        use_container_width=True
    )

    st.dataframe(
        yearly_rating,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------
    # ULASAN PER BULAN
    # --------------------------------------

    st.subheader("Jumlah Ulasan per Bulan")

    monthly_reviews_chart = plot_monthly_reviews(
        monthly_reviews
    )

    st.plotly_chart(
        monthly_reviews_chart,
        use_container_width=True
    )


# ==========================================
# MENU 5: BUSINESS INSIGHT
# ==========================================


elif menu == "Business Insight":
    st.title("Business Insight")

    st.write(
        "Ringkasan hasil analisis kepuasan pelanggan, "
        "diskusi produk, kualitas pelayanan, dan lokasi."
    )

    # Menjalankan seluruh analisis
    rating_result = analyze_ratings(data)
    product_result = analyze_products(data)
    service_result = analyze_service(data)
    location_result = analyze_locations(data)

    # MapReduce berdasarkan kelompok rating
    word_counts_by_group = run_mapreduce_by_rating(data)

    # Menghasilkan insight
    insights = generate_business_insights(
        rating_result,
        word_counts_by_group,
        product_result,
        service_result,
        location_result
    )

    st.subheader("Kesimpulan Analisis")

    for i, insight in enumerate(insights, start=1):
        st.markdown(f"**{i}.** {insight}")

    st.divider()

    st.subheader("Ringkasan Hasil Empat Analisis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rata-rata Rating",
            f"{rating_result['average_rating']:.2f}"
        )

        st.metric(
            "Total Penyebutan Produk",
            f"{product_result['total_product_mentions']:,}"
        )

    with col2:
        st.metric(
            "Total Penyebutan Pelayanan",
            f"{service_result['total_service_mentions']:,}"
        )

        st.metric(
            "Jumlah Lokasi",
            f"{location_result['total_locations']:,}"
        )

    st.caption(
        "Insight dibuat berdasarkan frekuensi dan statistik "
        "dataset. Penyebutan kata tidak selalu menunjukkan "
        "sentimen positif atau negatif."
    )



# ==========================================
# FOOTER
# ==========================================

st.sidebar.caption(
    "Project Big Data Analytics | Python + MapReduce"
)

st.caption(
    "Analisis Ulasan Pelanggan Starbucks | "
    "Big Data Project"
)
