import pytest
from transformers import AutoTokenizer
from chisel.labelers.bilo_labeler import BILOLabeler
from chisel.models.models import Token, EntitySpan


@pytest.fixture(scope="module")
def tokenizer():
    return AutoTokenizer.from_pretrained("bert-base-uncased")


def make_tokens(tokenizer, text):
    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    return [
        Token(
            id=input_id,
            text=tokenizer.convert_ids_to_tokens([input_id])[0],
            start=start,
            end=end
        )
        for input_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]

def test_bilo_labeler_single_token_entity(tokenizer):
    text = "Google announced a new feature."
    entity = EntitySpan(text="Google", start=0, end=6, label="ORG")

    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = [
        Token(
            id=input_id,
            text=tokenizer.convert_ids_to_tokens([input_id])[0],
            start=start,
            end=end
        )
        for input_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]

    labeler = BILOLabeler(subword_strategy="first")
    labels = labeler.label(tokens, [entity])

    assert labels[0] == "U-ORG"
    assert all(label == "O" for label in labels[1:])


def test_bilo_labeler_multi_token_entity(tokenizer):
    text = "Barack Obama visited Berlin."
    entity = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")

    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = [
        Token(
            id=input_id,
            text=tokenizer.convert_ids_to_tokens([input_id])[0],
            start=start,
            end=end
        )
        for input_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]

    labeler = BILOLabeler(subword_strategy="all")
    labels = labeler.label(tokens, [entity])

    entity_labels = [l for l in labels if l != "O"]
    assert entity_labels[0] == "B-PER"
    assert entity_labels[-1] == "L-PER"
    if len(entity_labels) > 2:
        for middle in entity_labels[1:-1]:
            assert middle == "I-PER"


def test_misaligned_entity_fail(tokenizer):
    text = "Apple released a product."
    tokens = make_tokens(tokenizer, text)

    # Deliberately misaligned entity span
    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BILOLabeler(misalignment_policy="fail")
    with pytest.raises(ValueError, match="No tokens align with entity span"):
        labeler.label(tokens, [entity])

def test_misaligned_entity_warn(tokenizer, caplog):
    text = "Apple released a product."
    tokens = make_tokens(tokenizer, text)

    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BILOLabeler(misalignment_policy="warn")
    with caplog.at_level("WARNING"):
        labels = labeler.label(tokens, [entity])

    assert "No tokens align with entity span" in caplog.text
    assert all(label == "O" for label in labels)

def test_misaligned_entity_skip(tokenizer):
    text = "Apple released a product."
    tokens = make_tokens(tokenizer, text)

    entity = EntitySpan(text="XYZ", start=100, end=103, label="MISC")

    labeler = BILOLabeler(misalignment_policy="skip")
    labels = labeler.label(tokens, [entity])

    assert all(label == "O" for label in labels)


@pytest.mark.parametrize("model_name", [
    "bert-base-uncased",        # WordPiece
    "roberta-base",             # BPE
    "albert-base-v2",           # SentencePiece
    "xlm-roberta-base",         # SPM+BPE
])
def test_bilo_labeler_multitoken_entity_on_various_tokenizers(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    text = "Barack Obama visited Berlin."
    entity = EntitySpan(text="Barack Obama", start=0, end=12, label="PER")

    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = [
        Token(
            id=token_id,
            text=tokenizer.convert_ids_to_tokens([token_id])[0],
            start=start,
            end=end
        )
        for token_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]

    labeler = BILOLabeler(subword_strategy="all")
    labels = labeler.label(tokens, [entity])
    entity_labels = [l for l in labels if l != "O"]

    if len(entity_labels) == 1:
        assert entity_labels[0].startswith("U-")
    else:
        assert entity_labels[0].startswith("B-")
        assert entity_labels[-1].startswith("L-")
        for l in entity_labels[1:-1]:
            assert l.startswith("I-")
