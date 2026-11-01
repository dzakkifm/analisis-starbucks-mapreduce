
import pandas as pd


def analyze_data_quality(df):

    total_rows = len(df)
    total_columns = len(df.columns)

    # Data kosong
    missing_values = df.isna().sum()

    # Duplikasi baris
    duplicate_rows = df.duplicated().sum()

    # Duplikasi teks ulasan
    if "review" in df.columns:
        reviews = (
            df["review"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        duplicate_reviews = reviews.dropna().duplicated().sum()
    else:
        duplicate_reviews = None

    # Analisis rating
    if "rating" in df.columns:
        valid_rating = df["rating"].between(1, 5)

        rating_count = valid_rating.sum()

        invalid_ratings = (
            df["rating"].notna() & ~valid_rating
        ).sum()

        average_rating = (
            df.loc[valid_rating, "rating"].mean()
        )
    else:
        rating_count = None
        invalid_ratings = None
        average_rating = None

    # Analisis tanggal
    if "date" in df.columns:
        valid_dates = df["date"].notna().sum()
        invalid_dates = df["date"].isna().sum()

        earliest_date = df["date"].min()
        latest_date = df["date"].max()
    else:
        valid_dates = None
        invalid_dates = None
        earliest_date = None
        latest_date = None

    # Lokasi unik
    if "location" in df.columns:
        unique_locations = df["location"].nunique()
    else:
        unique_locations = None

    summary = {
        "Total Baris": total_rows,
        "Total Kolom": total_columns,
        "Rating Valid": rating_count,
        "Rating Tidak Valid": invalid_ratings,
        "Rata-rata Rating": average_rating,
        "Baris Duplikat": duplicate_rows,
        "Teks Ulasan Duplikat": duplicate_reviews,
        "Tanggal Valid": valid_dates,
        "Tanggal Tidak Valid": invalid_dates,
        "Tanggal Paling Awal": earliest_date,
        "Tanggal Paling Akhir": latest_date,
        "Lokasi Unik": unique_locations
    }

    quality_summary = pd.DataFrame(
        list(summary.items()),
        columns=["Indikator", "Hasil"]
    )

    missing_summary = pd.DataFrame({
        "Kolom": missing_values.index,
        "Jumlah Kosong": missing_values.values,
        "Persentase Kosong (%)": (
            missing_values.values / total_rows * 100
        ).round(2)
    })

    return quality_summary, missing_summary


def get_rating_distribution(df):

    if "rating" not in df.columns:
        return pd.DataFrame(
            columns=["Rating", "Jumlah Ulasan"]
        )

    valid_data = df[
        df["rating"].between(1, 5)
    ]

    distribution = (
        valid_data["rating"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .sort_index()
        .reset_index()
    )

    distribution.columns = [
        "Rating",
        "Jumlah Ulasan"
    ]

    return distribution


if __name__ == "__main__":

    from src.data_loader import load_dataset

    data = load_dataset()

    quality, missing = analyze_data_quality(data)

    print("\nLAPORAN KUALITAS DATA")
    print("=" * 50)
    print(quality.to_string(index=False))

    print("\nDATA KOSONG PER KOLOM")
    print("=" * 50)
    print(missing.to_string(index=False))

    print("\nDISTRIBUSI RATING")
    print("=" * 50)
    print(
        get_rating_distribution(data).to_string(
            index=False
        )
    )
