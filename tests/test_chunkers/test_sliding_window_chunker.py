import pytest
from chisel.extraction.chunkers.sliding_window_chunker import SlidingWindowChunker
from chisel.extraction.models.models import Token, EntitySpan


def test_sliding_window_chunker_basic():
    text = "John lives in New York City. Mary works in San Francisco."

    tokens = [
        Token(id=0, text="John", start=0, end=4),
        Token(id=1, text="lives", start=5, end=10),
        Token(id=2, text="in", start=11, end=13),
        Token(id=3, text="New", start=14, end=17),
        Token(id=4, text="York", start=18, end=22),
        Token(id=5, text="City", start=23, end=27),
        Token(id=6, text=".", start=27, end=28),
        Token(id=7, text="Mary", start=29, end=33),
        Token(id=8, text="works", start=34, end=39),
        Token(id=9, text="in", start=40, end=42),
        Token(id=10, text="San", start=43, end=46),
        Token(id=11, text="Francisco", start=47, end=56),
        Token(id=12, text=".", start=56, end=57),
    ]

    entities = [
        EntitySpan(text="John", start=0, end=4, label="PER"),
        EntitySpan(text="New York City", start=14, end=27, label="LOC"),
        EntitySpan(text="Mary", start=29, end=33, label="PER"),
        EntitySpan(text="San Francisco", start=43, end=56, label="LOC"),
    ]

    chunker = SlidingWindowChunker(window_size=30, stride=20)
    chunks = chunker.chunk(text, tokens, entities)

    # Expecting 3 chunks
    assert len(chunks) == 3

    # Chunk 0
    assert chunks[0]["text"] == text[0:30]
    assert [t.text for t in chunks[0]["tokens"]] == [
        "John",
        "lives",
        "in",
        "New",
        "York",
        "City",
        ".",
    ]
    assert [(e.text, e.label) for e in chunks[0]["entities"]] == [
        ("John", "PER"),
        ("New York City", "LOC"),
    ]

    # Chunk 1
    assert chunks[1]["text"] == text[20:50]
    assert [t.text for t in chunks[1]["tokens"]] == [
        "City",
        ".",
        "Mary",
        "works",
        "in",
        "San",
    ]
    assert [(e.text, e.label) for e in chunks[1]["entities"]] == [("Mary", "PER")]

    # Chunk 2
    assert chunks[2]["text"] == text[40 : len(text)]
    assert [t.text for t in chunks[2]["tokens"]] == ["in", "San", "Francisco", "."]
    assert [(e.text, e.label) for e in chunks[2]["entities"]] == [
        ("San Francisco", "LOC")
    ]
