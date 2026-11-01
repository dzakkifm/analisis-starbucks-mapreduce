
import pandas as pd


def analyze_ratings(data):
    # Mengambil data yang memiliki rating valid
    valid_data = data.dropna(subset=["rating"]).copy()

    # Distribusi rating 1 sampai 5
    rating_counts = (
        valid_data["rating"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .sort_index()
    )

    # Persentase setiap rating
    rating_percentages = (
        rating_counts / rating_counts.sum() * 100
    )

    # Distribusi kelompok rating
    group_counts = (
        valid_data["rating_group"]
        .value_counts()
        .reindex(["low", "medium", "high"], fill_value=0)
    )

    group_percentages = (
        group_counts / group_counts.sum() * 100
    )

    # Statistik rating
    average_rating = valid_data["rating"].mean()
    median_rating = valid_data["rating"].median()

    return {
        "total_reviews": len(valid_data),
        "average_rating": average_rating,
        "median_rating": median_rating,
        "rating_counts": rating_counts,
        "rating_percentages": rating_percentages,
        "group_counts": group_counts,
        "group_percentages": group_percentages
    }


if __name__ == "__main__":
    from src.data_loader import load_dataset
    from src.preprocessing import preprocess_dataset

    data = load_dataset()
    processed_data = preprocess_dataset(data)

    results = analyze_ratings(processed_data)

    print("\nANALISIS RATING STARBUCKS")
    print("=" * 50)

    print(f"Total ulasan dengan rating: {results['total_reviews']}")
    print(f"Rata-rata rating: {results['average_rating']:.2f}")
    print(f"Median rating: {results['median_rating']:.2f}")

    print("\nDISTRIBUSI RATING")
    print("=" * 50)

    for rating in results["rating_counts"].index:
        count = results["rating_counts"][rating]
        percentage = results["rating_percentages"][rating]

        print(
            f"Rating {rating}: "
            f"{count} ulasan ({percentage:.2f}%)"
        )

    print("\nDISTRIBUSI KELOMPOK RATING")
    print("=" * 50)

    for group in results["group_counts"].index:
        count = results["group_counts"][group]
        percentage = results["group_percentages"][group]

        print(
            f"{group.upper()}: "
            f"{count} ulasan ({percentage:.2f}%)"
        )
