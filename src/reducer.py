
def reducer(shuffled_data):
    """
    Menjumlahkan frekuensi setiap kata.
    """

    reduced_data = {}

    for word, counts in shuffled_data.items():
        reduced_data[word] = sum(counts)

    return reduced_data


if __name__ == "__main__":
    sample_data = {
        "coffee": [1, 1],
        "good": [1, 1],
        "bad": [1]
    }

    result = reducer(sample_data)

    print("HASIL REDUCER")
    print("=" * 40)

    # Urutkan berdasarkan frekuensi terbesar
    sorted_result = sorted(
        result.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for word, count in sorted_result:
        print(f"{word}: {count}")
