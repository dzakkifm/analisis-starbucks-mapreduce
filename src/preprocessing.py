
import re
import pandas as pd

# Stopwords bahasa Inggris.
# Kata "not", "no", dan "nor" sengaja dipertahankan.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but",
    "is", "are", "was", "were", "be", "been",
    "to", "of", "in", "on", "at", "for",
    "with", "as", "by", "from", "this", "that",
    "it", "its", "i", "me", "my", "we", "our",
    "you", "your", "he", "she", "they", "them",
    "their", "am", "do", "does", "did",
    "have", "has", "had", "will", "would",
    "can", "could", "should", "very",
    "so", "too", "just", "also", "there",
    "here", "when", "where", "what", "which",
    "who", "how", "all", "any", "some",
    "more", "most", "much", "many",
    "than", "then", "if", "because",
    "about", "up", "out", "into", "over",
    "after", "before", "again"
}



def clean_text(text):
    """Membersihkan satu teks ulasan."""

    if pd.isna(text):
        return ""

    text = str(text).lower()
    # Samakan apostrof melengkung dengan apostrof biasa
    text = text.replace("’", "'").replace("‘", "'")

    # Normalisasi kontraksi bahasa Inggris
    contractions = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "can't": "cannot",
        "couldn't": "could not",
        "wouldn't": "would not",
        "shouldn't": "should not",
        "i'm": "i am",
        "i've": "i have",
        "i'd": "i would",
        "i'll": "i will",
        "it's": "it is",
        "that's": "that is",
        "there's": "there is",
        "we're": "we are",
        "they're": "they are",
        "you're": "you are"
    }

    for contraction, replacement in contractions.items():
        text = text.replace(contraction, replacement)

    # Hapus URL
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # Hapus karakter selain huruf dan spasi
    text = re.sub(r"[^a-z\s]", " ", text)

    # Pisahkan kata
    words = text.split()

    # Hapus stopwords
    words = [
        word for word in words
        if word not in STOPWORDS
    ]

    return " ".join(words)



def preprocess_dataset(df):
    """Membersihkan seluruh kolom review."""

    df = df.copy()

    df["review_clean"] = df["review"].apply(clean_text)

    # Kelompok rating
    def classify_rating(rating):
        if pd.isna(rating):
            return "unknown"
        elif rating <= 2:
            return "low"
        elif rating == 3:
            return "medium"
        else:
            return "high"

    df["rating_group"] = df["rating"].apply(classify_rating)

    return df


if __name__ == "__main__":
    print("\nTES PEMBERSIHAN KONTRAKSI")
contoh = [
    "I'd love it",
    "I've had bad experiences",
    "I don't like this coffee",
    "I'm happy"
]

for text in contoh:
    print(f"Sebelum: {text}")
    print(f"Sesudah: {clean_text(text)}")
    print()
    from src.data_loader import load_dataset

    data = load_dataset()
    processed_data = preprocess_dataset(data)

    print("\nHASIL PREPROCESSING")
    print("=" * 50)

    print("\nContoh teks sebelum dan sesudah:")
    print(
        processed_data[
            ["review", "review_clean", "rating", "rating_group"]
        ].head(10).to_string(index=False)
    )

    print("\nDistribusi kelompok rating:")
    print(
        processed_data["rating_group"]
        .value_counts()
        .to_string()
    )

    print("\nJumlah teks kosong setelah preprocessing:")
    print(
        (processed_data["review_clean"].str.strip() == "").sum()
    )
