import pytest
from chisel.extraction.chunkers.fixed_length_chunker import FixedLengthChunker
from chisel.extraction.models.models import Token, EntitySpan

def test_fixed_length_chunker_basic():
    tokens = [
        Token(id=0, text="John", start=0, end=4),
        Token(id=1, text="lives", start=5, end=10),
        Token(id=2, text="in", start=11, end=13),
        Token(id=3, text="New", start=14, end=17),
        Token(id=4, text="York", start=18, end=22),
        Token(id=5, text="City", start=23, end=27),
        Token(id=6, text=".", start=27, end=28),
    ]

    entities = [
        EntitySpan(text="John", start=0, end=4, label="PER"),
        EntitySpan(text="New York City", start=14, end=27, label="LOC"),
    ]

    chunker = FixedLengthChunker(max_tokens=4, overlap=1)
    chunks = chunker.chunk(tokens, entities)

    assert len(chunks) == 3

    # Chunk 0
    assert [t.text for t in chunks[0]["tokens"]] == ["John", "lives", "in", "New"]
    assert [(e.text, e.label) for e in chunks[0]["entities"]] == [("John", "PER")]

    # Chunk 1
    assert [t.text for t in chunks[1]["tokens"]] == ["New", "York", "City", "."]
    assert [(e.text, e.label) for e in chunks[1]["entities"]] == [("New York City", "LOC")]

    # Chunk 2
    assert [t.text for t in chunks[2]["tokens"]] == ["."]
    assert chunks[2]["entities"] == []
