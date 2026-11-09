
import pandas as pd


def analyze_locations(data, top_n=10):
    # Mengambil data lokasi dan rating
    location_data = data[["location", "rating"]].copy()

    # Membersihkan data lokasi
    location_data["location"] = (
        location_data["location"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    location_data.loc[
        location_data["location"] == "",
        "location"
    ] = "Unknown"

    # Mengubah rating menjadi numerik
    location_data["rating"] = pd.to_numeric(
        location_data["rating"],
        errors="coerce"
    )

    # Menghitung jumlah ulasan dan rata-rata rating
    location_summary = (
        location_data
        .groupby("location")
        .agg(
            total_reviews=("location", "count"),
            average_rating=("rating", "mean"),
            rated_reviews=("rating", "count")
        )
        .reset_index()
    )

    # Mengurutkan berdasarkan jumlah ulasan terbanyak
    top_locations = (
        location_summary
        .sort_values(
            by="total_reviews",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    # Mengurutkan lokasi berdasarkan rata-rata rating
    # Hanya lokasi dengan minimal satu rating yang dihitung
    top_rated_locations = (
        location_summary[
            location_summary["rated_reviews"] > 0
        ]
        .sort_values(
            by="average_rating",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    return {
        "total_locations": location_data[
            location_data["location"] != "Unknown"
        ]["location"].nunique(),

        "total_reviews": len(location_data),

        "top_locations": top_locations,

        "top_rated_locations": top_rated_locations,

        "location_summary": location_summary
    }
