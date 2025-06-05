import pytest
from chisel.extraction.models.models import Token, EntitySpan, TokenEntitySpan
from chisel.extraction.labelers.bilo_labeler import BILOLabeler

def test_bilou_labeler_single_token_span():
    tokens = [
        Token(id=1, text="Barack", start=0, end=6),
        Token(id=2, text="Obama", start=7, end=12),
        Token(id=3, text="visited", start=13, end=20),
    ]
    span = EntitySpan(text="Barack", start=0, end=6, label="PER")
    token_entity_span = TokenEntitySpan(entity=span, token_indices=[0])

    labeler = BILOLabeler()
    labels = labeler.label(tokens, [token_entity_span])
    assert labels == ["U-PER", "O", "O"]

def test_bilou_labeler_multi_token_span():
    tokens = [
        Token(id=1, text="Barack", start=0, end=6),
        Token(id=2, text="Obama", start=7, end=12),
        Token(id=3, text="visited", start=13, end=20),
    ]
    span = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")
    token_entity_span = TokenEntitySpan(entity=span, token_indices=[0, 1])

    labeler = BILOLabeler()
    labels = labeler.label(tokens, [token_entity_span])
    assert labels == ["B-PER", "L-PER", "O"]

def test_bilou_labeler_multiple_spans():
    tokens = [
        Token(id=1, text="Barack", start=0, end=6),
        Token(id=2, text="Obama", start=7, end=12),
        Token(id=3, text="met", start=13, end=16),
        Token(id=4, text="Angela", start=17, end=23),
        Token(id=5, text="Merkel", start=24, end=30),
    ]
    span1 = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")
    span2 = EntitySpan(text="Angela Merkel", start=17, end=30, label="PER")
    token_entity_spans = [
        TokenEntitySpan(entity=span1, token_indices=[0, 1]),
        TokenEntitySpan(entity=span2, token_indices=[3, 4])
    ]

    labeler = BILOLabeler()
    labels = labeler.label(tokens, token_entity_spans)
    assert labels == ["B-PER", "L-PER", "O", "B-PER", "L-PER"]

def test_bilou_labeler_inside_span():
    tokens = [
        Token(id=1, text="The", start=0, end=3),
        Token(id=2, text="Barack", start=4, end=10),
        Token(id=3, text="Hussein", start=11, end=18),
        Token(id=4, text="Obama", start=19, end=24),
    ]
    span = EntitySpan(text="Barack Hussein Obama", start=4, end=24, label="PER")
    token_entity_span = TokenEntitySpan(entity=span, token_indices=[1, 2, 3])

    labeler = BILOLabeler()
    labels = labeler.label(tokens, [token_entity_span])
    assert labels == ["O", "B-PER", "I-PER", "L-PER"]
