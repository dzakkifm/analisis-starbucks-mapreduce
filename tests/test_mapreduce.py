
from src.mapper import mapper
from src.shuffle import shuffle
from src.reducer import reducer
from src.mapreduce import run_mapreduce, get_top_words


def test_mapper():
    result = mapper("coffee starbucks coffee")

    assert result == [
        ("coffee", 1),
        ("starbucks", 1),
        ("coffee", 1)
    ]


def test_mapper_empty_text():
    assert mapper("") == []


def test_shuffle():
    mapped_data = [
        ("coffee", 1),
        ("starbucks", 1),
        ("coffee", 1)
    ]

    result = shuffle(mapped_data)

    assert result == {
        "coffee": [1, 1],
        "starbucks": [1]
    }


def test_reducer():
    shuffled_data = {
        "coffee": [1, 1, 1],
        "starbucks": [1, 1]
    }

    result = reducer(shuffled_data)

    assert result == {
        "coffee": 3,
        "starbucks": 2
    }


def test_run_mapreduce():
    texts = [
        "coffee starbucks",
        "coffee good"
    ]

    result = run_mapreduce(texts)

    assert result == {
        "coffee": 2,
        "starbucks": 1,
        "good": 1
    }


def test_get_top_words():
    word_counts = {
        "coffee": 10,
        "starbucks": 5,
        "service": 3
    }

    result = get_top_words(word_counts, 2)

    assert result == [
        ("coffee", 10),
        ("starbucks", 5)
    ]
