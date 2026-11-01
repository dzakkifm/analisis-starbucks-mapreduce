
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "reviews_data.csv"


def normalize_columns(df):
    # Rapikan nama kolom
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Hapus kolom tambahan hasil pembacaan CSV
    unwanted_columns = [
        col for col in df.columns
        if col.startswith("unnamed")
    ]

    if unwanted_columns:
        df = df.drop(columns=unwanted_columns)
        print(f"Kolom tambahan dihapus: {unwanted_columns}")

    return df


def load_dataset(file_path=DATA_PATH):
    """Membaca dan menyiapkan dataset."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {file_path}"
        )

    try:
        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            encoding="utf-8-sig"
        )
    except Exception as error:
        raise ValueError(
            f"Gagal membaca dataset: {error}"
        )

    if df.empty:
        raise ValueError("Dataset tidak memiliki data.")

    df = normalize_columns(df)

    # Kolom review wajib tersedia
    if "review" not in df.columns:
        raise ValueError(
            "Kolom 'Review' tidak ditemukan."
        )

    # Membersihkan teks ulasan
    df["review"] = (
        df["review"]
        .astype("string")
        .str.strip()
    )

    # Mengubah rating menjadi numerik
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

    # Memperbaiki format tanggal
    if "date" in df.columns:
        date_text = (
            df["date"]
            .astype("string")
            .str.strip()
            .str.replace(
                r"^Reviewed\s+",
                "",
                regex=True
            )
        )

        df["date"] = pd.to_datetime(
            date_text,
            format="mixed",
            errors="coerce"
        )

    return df


if __name__ == "__main__":
    data = load_dataset()

    print("DATASET BERHASIL DIMUAT")
    print("=" * 40)

    print(f"Jumlah baris : {len(data)}")
    print(f"Jumlah kolom : {len(data.columns)}")

    print("\nNama kolom:")
    print(data.columns.tolist())

    print("\nContoh data:")
    print(data.head())

    if "date" in data.columns:
        print("\nContoh tanggal:")
        print(data["date"].head())
