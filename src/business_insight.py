
def generate_business_insights(
    rating_result,
    word_counts_by_group,
    product_result=None,
    service_result=None,
    location_result=None
):
    insights = []

    # 1. Customer Satisfaction
    group_counts = rating_result["group_counts"]
    group_percentages = rating_result["group_percentages"]

    low_count = group_counts["low"]
    medium_count = group_counts["medium"]
    high_count = group_counts["high"]

    low_percentage = group_percentages["low"]
    high_percentage = group_percentages["high"]

    average_rating = rating_result["average_rating"]

    insights.append(
        f"Customer Satisfaction: Kelompok rating LOW memiliki "
        f"{low_count} ulasan ({low_percentage:.2f}%). "
        f"Rata-rata rating keseluruhan adalah {average_rating:.2f}."
    )

    insights.append(
        f"Sebanyak {high_count} ulasan ({high_percentage:.2f}%) "
        f"termasuk kelompok HIGH, sedangkan kelompok MEDIUM "
        f"memiliki {medium_count} ulasan."
    )

    # 2. Product Discussion
    if product_result:
        top_products = product_result["top_products"]

        if top_products:
            product_name, product_count = top_products[0]

            insights.append(
                f"Product Discussion: Istilah produk yang paling "
                f"sering disebut adalah '{product_name}' dengan "
                f"{product_count} kemunculan."
            )

    # 3. Service Quality
    if service_result:
        top_service = service_result["top_service_words"]

        if top_service:
            service_name, service_count = top_service[0]

            insights.append(
                f"Service Quality: Istilah pelayanan yang paling "
                f"sering muncul adalah '{service_name}' dengan "
                f"{service_count} kemunculan."
            )

    # 4. Location Analysis
    if location_result:
        top_locations = location_result["top_locations"]

        if not top_locations.empty:
            top_location = top_locations.iloc[0]

            insights.append(
                f"Location Analysis: Lokasi dengan jumlah ulasan "
                f"terbanyak adalah '{top_location['location']}' "
                f"dengan {top_location['total_reviews']} ulasan."
            )

    insights.append(
        "Catatan: Hasil analisis menggambarkan dataset ulasan "
        "yang digunakan dan tidak mewakili seluruh pelanggan "
        "atau gerai Starbucks."
    )

    return insights
