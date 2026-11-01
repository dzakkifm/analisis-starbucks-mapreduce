
import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.preprocessing import preprocess_dataset
from src.mapreduce import run_mapreduce, get_top_words
from src.rating_analysis import analyze_ratings
from src.temporal_analysis import analyze_temporal
from src.visualization import (
    plot_rating_distribution,
    plot_yearly_reviews,
    plot_yearly_rating,
    plot_monthly_reviews
)
from src.business_insight import generate_business_insights


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

    st.header("Business Insight dan Rekomendasi")

    st.write(
        "Bagian ini menyajikan temuan bisnis berdasarkan "
        "hasil analisis rating dan frekuensi kata menggunakan MapReduce."
    )

    # --------------------------------------
    # MAPREDUCE BERDASARKAN KELOMPOK RATING
    # --------------------------------------

    word_counts_by_group = {}

    for group in ["low", "medium", "high"]:

        group_data = data[
            data["rating_group"] == group
        ]

        group_texts = group_data["review_clean"].dropna()
        group_texts = group_texts[
            group_texts.str.strip() != ""
        ]

        word_counts_by_group[group] = run_mapreduce(
            group_texts
        )

    # --------------------------------------
    # GENERATE INSIGHT
    # --------------------------------------

    insights = generate_business_insights(
        rating_result,
        word_counts_by_group
    )

    # --------------------------------------
    # TAMPILKAN INSIGHT
    # --------------------------------------

    for index, insight in enumerate(insights, start=1):

        st.subheader(
            f"{index}. {insight['judul']}"
        )

        st.markdown(
            f"**Temuan:** {insight['temuan']}"
        )

        st.markdown(
            f"**Rekomendasi:** {insight['rekomendasi']}"
        )

        st.divider()

    st.caption(
        "Catatan: Insight merupakan interpretasi awal berdasarkan "
        "data ulasan yang tersedia. Frekuensi kata tidak secara "
        "langsung membuktikan penyebab kepuasan atau ketidakpuasan pelanggan."
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
