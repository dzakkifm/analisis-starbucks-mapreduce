
def generate_business_insights(rating_result, word_counts_by_group):
    """
    Menghasilkan insight bisnis berdasarkan hasil analisis rating
    dan frekuensi kata dari MapReduce.
    """

    insights = []

    average_rating = rating_result["average_rating"]
    rating_groups = rating_result["group_counts"]
    total_ratings = rating_result["total_reviews"]

    low_count = rating_groups.get("low", 0)
    medium_count = rating_groups.get("medium", 0)
    high_count = rating_groups.get("high", 0)

    low_percentage = (low_count / total_ratings * 100) if total_ratings else 0
    high_percentage = (high_count / total_ratings * 100) if total_ratings else 0

    # Insight 1: Kondisi kepuasan pelanggan
    insights.append({
        "judul": "Dominasi Rating Rendah",
        "temuan": (
            f"Sebanyak {low_percentage:.2f}% ulasan dengan rating valid "
            "termasuk dalam kelompok rating rendah (1–2)."
        ),
        "rekomendasi": (
            "Evaluasi kualitas pelayanan, proses pemesanan, dan pengalaman "
            "pelanggan untuk menemukan faktor yang menyebabkan ketidakpuasan."
        )
    })

    # Insight 2: Rating tinggi
    insights.append({
        "judul": "Peluang Mempertahankan Pengalaman Positif",
        "temuan": (
            f"Sebanyak {high_percentage:.2f}% ulasan dengan rating valid "
            "termasuk dalam kelompok rating tinggi (4–5)."
        ),
        "rekomendasi": (
            "Identifikasi aspek layanan yang sering muncul dalam ulasan "
            "positif dan pertahankan konsistensi kualitasnya."
        )
    })

    # Insight 3: Kata yang sering muncul pada ulasan rendah
    low_words = word_counts_by_group.get("low", {})
    top_low_words = sorted(
        low_words.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    insights.append({
        "judul": "Topik pada Ulasan Rating Rendah",
        "temuan": (
            "Kata yang paling sering muncul: "
            + ", ".join(word for word, count in top_low_words[:5])
        ),
        "rekomendasi": (
            "Gunakan kata-kata tersebut sebagai petunjuk awal untuk "
            "meninjau topik keluhan pelanggan. Periksa kembali konteks "
            "kalimat sebelum mengambil keputusan."
        )
    })

    # Insight 4: Rata-rata rating
    insights.append({
        "judul": "Evaluasi Rata-rata Rating",
        "temuan": f"Rata-rata rating pelanggan adalah {average_rating:.2f} dari 5.",
        "rekomendasi": (
            "Lakukan evaluasi berkala terhadap kualitas produk dan pelayanan, "
            "kemudian pantau perubahan rating setelah perbaikan dilakukan."
        )
    })

    return insights
