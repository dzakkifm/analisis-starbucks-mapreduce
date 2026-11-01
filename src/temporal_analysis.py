
import pandas as pd


def analyze_temporal(data):
    # Salin data agar data asli tidak berubah
    df = data.copy()

    # Pastikan kolom tanggal bertipe datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Menghapus data yang tidak memiliki tanggal valid
    df = df.dropna(subset=["date"])

    # Membuat kolom tahun dan bulan
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Analisis jumlah ulasan per tahun
    yearly_reviews = (
        df.groupby("year")
        .size()
        .reset_index(name="total_reviews")
    )

    # Analisis rata-rata rating per tahun
    yearly_rating = (
        df.dropna(subset=["rating"])
        .groupby("year")["rating"]
        .mean()
        .reset_index(name="average_rating")
    )

    # Analisis jumlah ulasan per bulan
    monthly_reviews = (
        df.groupby("month")
        .size()
        .reset_index(name="total_reviews")
        .sort_values("month")
    )

    return yearly_reviews, yearly_rating, monthly_reviews


if __name__ == "__main__":
    from src.data_loader import load_dataset

    data = load_dataset()

    yearly_reviews, yearly_rating, monthly_reviews = (
        analyze_temporal(data)
    )

    print("\nANALISIS TEMPORAL STARBUCKS")
    print("=" * 50)

    print("\nJUMLAH ULASAN PER TAHUN")
    print(yearly_reviews.to_string(index=False))

    print("\nRATA-RATA RATING PER TAHUN")
    print(yearly_rating.to_string(index=False))

    print("\nJUMLAH ULASAN PER BULAN")
    print(monthly_reviews.to_string(index=False))
