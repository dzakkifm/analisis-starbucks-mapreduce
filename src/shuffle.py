
from collections import defaultdict


def shuffle(mapped_data):
    """
    Mengelompokkan data berdasarkan kata (key).
    """

    grouped_data = defaultdict(list)

    for word, count in mapped_data:
        grouped_data[word].append(count)

    return dict(grouped_data)


if __name__ == "__main__":
    sample_data = [
        ("coffee", 1),
        ("good", 1),
        ("coffee", 1),
        ("bad", 1),
        ("good", 1),
    ]

    result = shuffle(sample_data)

    print("HASIL SHUFFLE")
    print("=" * 40)

    for word, counts in result.items():
        print(f"{word}: {counts}")
