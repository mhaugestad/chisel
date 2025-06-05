from chisel.extraction.models.models import Token, EntitySpan, TokenEntitySpan
from chisel.extraction.labelers.bio_labeler import BIOLabeler

def test_bio_labeler_single_token_span():
    tokens = [
        Token(id=1, text="Barack", start=0, end=6),
        Token(id=2, text="Obama", start=7, end=12),
        Token(id=3, text="visited", start=13, end=20),
    ]
    span = EntitySpan(text="Barack", start=0, end=6, label="PER")
    token_entity_span = TokenEntitySpan(entity=span, token_indices=[0])

    labeler = BIOLabeler()
    labels = labeler.label(tokens, [token_entity_span])
    assert labels == ["B-PER", "O", "O"]

def test_bio_labeler_multi_token_span():
    tokens = [
        Token(id=1, text="Barack", start=0, end=6),
        Token(id=2, text="Obama", start=7, end=12),
        Token(id=3, text="visited", start=13, end=20),
    ]
    span = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")
    token_entity_span = TokenEntitySpan(entity=span, token_indices=[0, 1])

    labeler = BIOLabeler()
    labels = labeler.label(tokens, [token_entity_span])
    assert labels == ["B-PER", "I-PER", "O"]

def test_bio_labeler_multiple_spans():
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

    labeler = BIOLabeler()
    labels = labeler.label(tokens, token_entity_spans)
    assert labels == ["B-PER", "I-PER", "O", "B-PER", "I-PER"]
