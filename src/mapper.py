
def mapper(text):
    """
    Mengubah teks menjadi pasangan (kata, 1).
    """

    if not isinstance(text, str):
        return []

    words = text.split()

    mapped_data = []

    for word in words:
        mapped_data.append((word, 1))

    return mapped_data


if __name__ == "__main__":
    sample_text = "coffee good coffee bad"

    result = mapper(sample_text)

    print("HASIL MAPPER")
    print("=" * 40)

    for item in result:
        print(item)
