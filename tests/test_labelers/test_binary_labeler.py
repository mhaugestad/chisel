import pytest
from transformers import AutoTokenizer
from chisel.extraction.labelers.binary_labeler import BinaryLabeler
from chisel.extraction.models.models import Token, EntitySpan


@pytest.fixture(scope="module")
def tokenizer():
    return AutoTokenizer.from_pretrained("bert-base-uncased")


def tokenize(tokenizer, text):
    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    return [
        Token(
            id=token_id,
            text=tokenizer.convert_ids_to_tokens([token_id])[0],
            start=start,
            end=end
        )
        for token_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]


def test_binary_labeler_first_strategy(tokenizer):
    text = "Barack Obama visited Berlin."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")

    labeler = BinaryLabeler(subword_strategy="first")
    labels = labeler.label(tokens, [entity])

    assert labels.count("ENTITY") == 1
    assert all(l in {"ENTITY", "O"} for l in labels)


def test_binary_labeler_all_strategy(tokenizer):
    text = "Barack Obama visited Berlin."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")

    labeler = BinaryLabeler(subword_strategy="all")
    labels = labeler.label(tokens, [entity])

    assert labels.count("ENTITY") >= 2
    assert all(l in {"ENTITY", "O"} for l in labels)


def test_binary_labeler_strict_strategy_exact_match(tokenizer):
    text = "Barack Obama visited Berlin."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")

    labeler = BinaryLabeler(subword_strategy="strict")
    labels = labeler.label(tokens, [entity])

    assert "ENTITY" in labels
    assert all(l in {"ENTITY", "O"} for l in labels)


def test_binary_labeler_misaligned_fail(tokenizer):
    text = "Apple released a product."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BinaryLabeler(misalignment_policy="fail")

    with pytest.raises(ValueError, match="No tokens align with entity span"):
        labeler.label(tokens, [entity])


def test_binary_labeler_misaligned_warn(tokenizer, caplog):
    text = "Apple released a product."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BinaryLabeler(misalignment_policy="warn")

    with caplog.at_level("WARNING"):
        labels = labeler.label(tokens, [entity])

    assert "No tokens align with entity span" in caplog.text
    assert all(l == "O" for l in labels)


def test_binary_labeler_misaligned_skip(tokenizer):
    text = "Apple released a product."
    tokens = tokenize(tokenizer, text)
    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BinaryLabeler(misalignment_policy="skip")
    labels = labeler.label(tokens, [entity])

    assert all(l == "O" for l in labels)
