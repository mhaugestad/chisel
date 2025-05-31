from chisel.extraction.validators.bio_alignment_validator import BIOAlignmentValidator
from chisel.extraction.models.models import Token, EntitySpan
import pytest

def test_bio_alignment_validator_success():
    tokens = [
        Token(id=0, text="Barack", start=0, end=6),
        Token(id=1, text="Obama", start=7, end=12),
        Token(id=2, text="is", start=13, end=15),
        Token(id=3, text="here", start=16, end=20),
    ]
    labels = ["B-PER", "I-PER", "O", "O"]
    spans = [
        EntitySpan(text="BarackObama", start=0, end=12, label="PER")
    ]

    validator = BIOAlignmentValidator()
    with pytest.raises(ValueError):
        # This should raise an error because the span text does not match the token labels
        validator.validate("BarackObama", tokens, spans, labels)


def test_bio_alignment_validator_mismatch():
    tokens = [
        Token(id=0, text="Barack", start=0, end=6),
        Token(id=1, text="Obama", start=7, end=12),
        Token(id=2, text="is", start=13, end=15),
        Token(id=3, text="here", start=16, end=20),
    ]
    labels = ["B-PER", "I-PER", "O", "O"]
    spans = [
        EntitySpan(text="Barack Obamo", start=0, end=12, label="PER")  # typo here
    ]

    validator = BIOAlignmentValidator()
    with pytest.raises(ValueError) as exc_info:
        # This should raise an error because the span text does not match the token labels
        validator.validate("Barack Obamo", tokens, spans, labels)