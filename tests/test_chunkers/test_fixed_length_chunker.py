import pytest
from chisel.extraction.chunkers.fixed_length_chunker import FixedLengthTokenChunker
from chisel.extraction.models.models import Token, EntitySpan, TokenEntitySpan


@pytest.fixture
def simple_data():
    tokens = [
        Token(id=i, text=f"T{i}", start=i*2, end=(i+1)*2)
        for i in range(10)
    ]
    # Entity from token index 2 to 4 (inclusive)
    entity_span = EntitySpan(text="T2T3T4", start=4, end=10, label="ENT")
    token_entity = TokenEntitySpan(entity=entity_span, token_indices=[2, 3, 4])

    return tokens, [token_entity]


def test_fixed_length_chunking_no_overlap(simple_data):
    tokens, token_entities = simple_data
    chunker = FixedLengthTokenChunker(max_tokens=5, overlap=0)
    token_chunks, entity_chunks = chunker.chunk(tokens, token_entities)

    assert len(token_chunks) == 2
    assert all(len(chunk) <= 5 for chunk in token_chunks)

    # Check that the entity is in the correct chunk
    assert len(entity_chunks[0]) == 1
    assert entity_chunks[1] == []


def test_fixed_length_chunking_with_overlap(simple_data):
    tokens, token_entities = simple_data
    chunker = FixedLengthTokenChunker(max_tokens=5, overlap=2)
    token_chunks, entity_chunks = chunker.chunk(tokens, token_entities)

    assert len(token_chunks) == 3
    assert all(len(chunk) <= 5 for chunk in token_chunks)

    # Check if the entity appears in the correct overlapping chunk
    found = any(e.entity.label == "ENT" for chunk in entity_chunks for e in chunk)
    assert found


def test_no_entities_still_chunks():
    tokens = [
        Token(id=i, text=f"T{i}", start=i*2, end=(i+1)*2)
        for i in range(6)
    ]
    chunker = FixedLengthTokenChunker(max_tokens=3, overlap=1)
    token_chunks, entity_chunks = chunker.chunk(tokens, [])

    assert len(token_chunks) == 3
    assert all(isinstance(chunk, list) for chunk in token_chunks)
    assert all(ec == [] for ec in entity_chunks)
