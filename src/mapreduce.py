
from collections import Counter

from src.mapper import mapper
from src.shuffle import shuffle
from src.reducer import reducer


def run_mapreduce(texts):
    """
    Menjalankan proses MapReduce pada kumpulan teks.
    """

    # Tahap 1: Mapper
    mapped_data = []

    for text in texts:
        mapped_data.extend(mapper(text))

    # Tahap 2: Shuffle
    shuffled_data = shuffle(mapped_data)

    # Tahap 3: Reducer
    reduced_data = reducer(shuffled_data)

    return reduced_data


def get_top_words(word_counts, top_n=20):
    """
    Mengambil kata dengan frekuensi tertinggi.
    """

    sorted_words = sorted(
        word_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_words[:top_n]

def run_mapreduce_by_rating(data, top_n=15):
    groups = ["low", "medium", "high"]

    for group in groups:
        group_data = data[data["rating_group"] == group]

        texts = group_data["review_clean"].dropna()
        texts = texts[texts.str.strip() != ""]

        word_counts = run_mapreduce(texts)
        top_words = get_top_words(word_counts, top_n)

        print(f"\nHASIL MAPREDUCE RATING: {group.upper()}")
        print("=" * 50)
        print(f"Jumlah ulasan: {len(texts)}")
        print(f"Jumlah kata unik: {len(word_counts)}")
        print("\nKata paling sering muncul:")

        for word, count in top_words:
            print(f"{word:<20} {count}")


if __name__ == "__main__":
    from src.data_loader import load_dataset
    from src.preprocessing import preprocess_dataset

    # Membaca dataset
    data = load_dataset()

    # Preprocessing
    processed_data = preprocess_dataset(data)

    # Mengambil teks ulasan yang tidak kosong
    texts = processed_data["review_clean"].dropna()

    # Menjalankan MapReduce
    results = run_mapreduce(texts)

    # Menampilkan 20 kata teratas
    top_words = get_top_words(results, top_n=20)

    print("\nHASIL MAPREDUCE STARBUCKS")
    print("=" * 50)

    print(f"Total ulasan diproses: {len(texts)}")
    print(f"Total kata unik: {len(results)}")

    print("\n20 KATA PALING SERING MUNCUL")
    print("=" * 50)

    for word, count in top_words:
        print(f"{word:<20} {count}")

    # Menjalankan MapReduce berdasarkan kelompok rating
    run_mapreduce_by_rating(processed_data)