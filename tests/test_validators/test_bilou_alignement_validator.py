from chisel.validators.bilou_alignement_validator import BILOUAlignmentValidator
from chisel.models.models import Token, EntitySpan


def test_bilou_alignment_validator_success():
    tokens = [
        Token(id=0, text="Barack", start=0, end=6),
        Token(id=1, text="Obama", start=7, end=12),
        Token(id=2, text="is", start=13, end=15),
    ]
    labels = ["B-PER", "L-PER", "O"]
    spans = [EntitySpan(text="BarackObama", start=0, end=12, label="PER")]
    validator = BILOUAlignmentValidator()
    assert not validator.validate(tokens, labels, spans)


def test_bilou_alignment_validator_unit_success():
    tokens = [Token(id=0, text="Obama", start=0, end=5)]
    labels = ["U-PER"]
    spans = [EntitySpan(text="Obama", start=0, end=5, label="PER")]
    validator = BILOUAlignmentValidator()
    assert not validator.validate(tokens, labels, spans)


def test_bilou_alignment_validator_missing_span():
    tokens = [Token(id=0, text="Obama", start=0, end=5)]
    labels = ["U-PER"]
    spans = []  # no span provided
    validator = BILOUAlignmentValidator()
    errors = validator.validate(tokens, labels, spans)
    assert len(errors) == 1
    assert "No span found" in errors[0]


def test_bilou_alignment_validator_mismatch():
    tokens = [
        Token(id=0, text="Barack", start=0, end=6),
        Token(id=1, text="Obama", start=7, end=12),
    ]
    labels = ["B-PER", "L-PER"]
    spans = [EntitySpan(text="Barack Obamo", start=0, end=12, label="PER")]  # typo
    validator = BILOUAlignmentValidator()
    errors = validator.validate(tokens, labels, spans)
    assert any("Mismatch" in e for e in errors)
