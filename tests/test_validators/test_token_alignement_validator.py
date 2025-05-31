import pytest
from transformers import AutoTokenizer
from chisel.extraction.models.models import Token, EntitySpan
from chisel.extraction.validators.token_alignement_validator import TokenAlignmentValidator


@pytest.fixture
def tokenizer():
    return AutoTokenizer.from_pretrained("bert-base-cased")


@pytest.fixture
def tokens_and_labels(tokenizer):
    text = "Barack Obama was born in Hawaii."
    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = [
        Token(id=tid, text=tokenizer.convert_ids_to_tokens(tid), start=start, end=end)
        for tid, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]
    labels = ["B-PER", "I-PER", "O", "O", "O", "B-LOC", "O"]
    return text, tokens, labels


@pytest.fixture
def entities():
    return [
        EntitySpan(text="Barack Obama", start=0, end=12, label="PER"),
        EntitySpan(text="Hawaii", start=25, end=31, label="LOC")
    ]


def test_token_alignment_success(tokenizer, tokens_and_labels, entities):
    text, tokens, labels = tokens_and_labels
    validator = TokenAlignmentValidator(tokenizer=tokenizer)
    validator.validate(text=text, tokens=tokens, entities=entities, labels=labels)


def test_token_alignment_fail(tokenizer, tokens_and_labels):
    text, tokens, labels = tokens_and_labels
    entities = [
        EntitySpan(text="Barack Hussein Obama", start=0, end=20, label="PER")
    ]
    validator = TokenAlignmentValidator(tokenizer=tokenizer)
    with pytest.raises(ValueError):
        validator.validate(text=text, tokens=tokens, entities=entities, labels=labels)