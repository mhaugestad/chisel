import pytest
from chisel.extraction.models.models import Token, TokenEntitySpan, EntitySpan
from chisel.extraction.labelers.binary_labeler import BinaryLabeler

@pytest.fixture
def sample_tokens():
    return [
        Token(id=0, text="Barack", start=0, end=6),
        Token(id=1, text="Obama", start=7, end=12),
        Token(id=2, text="visited", start=13, end=20),
        Token(id=3, text="Paris", start=21, end=26),
        Token(id=4, text=".", start=26, end=27),
    ]

def test_binary_labeler_entity_assignment(sample_tokens):
    token_entity_spans = [
        TokenEntitySpan(entity=EntitySpan(text="Barack Obama", start=0, end=12, label="PER"), token_indices=[0, 1]),
        TokenEntitySpan(entity=EntitySpan(text="Paris", start=21, end=26, label="LOC"), token_indices=[3]),
    ]

    labeler = BinaryLabeler()
    labels = labeler.label(sample_tokens, token_entity_spans)

    assert labels == ["ENTITY", "ENTITY", "O", "ENTITY", "O"]

def test_binary_labeler_no_entities(sample_tokens):
    token_entity_spans = []

    labeler = BinaryLabeler()
    labels = labeler.label(sample_tokens, token_entity_spans)

    assert labels == ["O", "O", "O", "O", "O"]
