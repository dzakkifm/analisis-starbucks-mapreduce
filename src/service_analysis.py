
from src.mapreduce import run_mapreduce, get_top_words


SERVICE_KEYWORDS = {
    "service", "staff", "employee", "employees",
    "barista", "worker", "workers", "manager",
    "friendly", "rude", "polite", "helpful",
    "customer", "wait", "waiting", "slow",
    "fast", "attitude", "behavior", "professional",
    "cashier", "order", "complaint", "problem",
    "support", "serve", "served", "team"
}


def analyze_service(data, top_n=10):
    # Mengambil teks ulasan yang sudah dibersihkan
    texts = data["review_clean"].dropna()
    texts = texts[texts.str.strip() != ""]

    # Menghitung seluruh frekuensi kata menggunakan MapReduce
    all_word_counts = run_mapreduce(texts)

    # Memfilter kata yang berkaitan dengan pelayanan
    service_counts = {
        word: count
        for word, count in all_word_counts.items()
        if word in SERVICE_KEYWORDS
    }

    top_service_words = get_top_words(service_counts, top_n)

    # Analisis berdasarkan kelompok rating
    service_by_rating = {}

    for group in ["low", "medium", "high"]:
        group_data = data[data["rating_group"] == group]

        group_texts = group_data["review_clean"].dropna()
        group_texts = group_texts[group_texts.str.strip() != ""]

        group_word_counts = run_mapreduce(group_texts)

        group_service_counts = {
            word: count
            for word, count in group_word_counts.items()
            if word in SERVICE_KEYWORDS
        }

        service_by_rating[group] = get_top_words(
            group_service_counts,
            top_n
        )

    return {
        "total_reviews": len(texts),
        "total_service_mentions": sum(service_counts.values()),
        "service_counts": service_counts,
        "top_service_words": top_service_words,
        "service_by_rating": service_by_rating
    }
