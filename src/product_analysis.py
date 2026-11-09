
from src.mapreduce import run_mapreduce, get_top_words


# Istilah produk dan minuman yang akan dianalisis.
# Daftar ini dapat dikembangkan berdasarkan isi dataset.

PRODUCT_KEYWORDS = {
    "coffee",
    "drink",
    "drinks",
    "espresso",
    "latte",
    "cappuccino",
    "frappuccino",
    "mocha",
    "americano",
    "macchiato",
    "tea",
    "food",
    "sandwich",
    "cake",
    "pastry",
    "muffin",
    "cookie",
    "chocolate",
    "milk",
    "juice",
    "water",
    "smoothie",
    "coldbrew",
    "brew"
}


def analyze_products(data, top_n=10):
    """
    Menganalisis frekuensi penyebutan produk dan minuman
    berdasarkan teks ulasan menggunakan MapReduce.
    """

    # Mengambil ulasan yang sudah dibersihkan
    texts = data["review_clean"].dropna()
    texts = texts[texts.str.strip() != ""]

    # Menjalankan MapReduce pada seluruh ulasan
    all_word_counts = run_mapreduce(texts)

    # Memfilter kata yang termasuk kategori produk
    product_counts = {
        word: count
        for word, count in all_word_counts.items()
        if word in PRODUCT_KEYWORDS
    }

    # Mengurutkan hasil berdasarkan frekuensi
    top_products = get_top_words(
        product_counts,
        top_n
    )

    # Analisis produk berdasarkan kelompok rating
    rating_groups = ["low", "medium", "high"]

    product_by_rating = {}

    for group in rating_groups:

        group_data = data[
            data["rating_group"] == group
        ]

        group_texts = group_data["review_clean"].dropna()
        group_texts = group_texts[
            group_texts.str.strip() != ""
        ]

        # MapReduce untuk masing-masing kelompok rating
        group_word_counts = run_mapreduce(group_texts)

        group_products = {
            word: count
            for word, count in group_word_counts.items()
            if word in PRODUCT_KEYWORDS
        }

        product_by_rating[group] = get_top_words(
            group_products,
            top_n
        )

    return {
        "total_reviews": len(texts),
        "total_product_mentions": sum(product_counts.values()),
        "product_counts": product_counts,
        "top_products": top_products,
        "product_by_rating": product_by_rating
    }
