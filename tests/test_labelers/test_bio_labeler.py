import pytest
from chisel.extraction.labelers.bio_labeler import BIOLabeler
from chisel.extraction.models.models import Token, EntitySpan
from transformers import AutoTokenizer

@pytest.mark.parametrize("strategy,expected_labels", [
    ("first", ["B-ORG", "O"]),
    ("all", ["B-ORG", "I-ORG"]),
    ("strict", ["O", "O"]),  # since no full token matches span exactly
])
def test_subword_alignment_strategies(strategy, expected_labels):
    tokens = [
        Token(id=1, text="▁Micro", start=0, end=6),     # subword 1
        Token(id=2, text="soft", start=6, end=10),      # subword 2
    ]
    entities = [
        EntitySpan(text="Microsoft", start=0, end=10, label="ORG")
    ]
    
    labeler = BIOLabeler(subword_strategy=strategy)
    labels = labeler.label(tokens, entities)
    assert labels == expected_labels


def make_token(id, text, start, end):
    return Token(id=id, text=text, start=start, end=end)

def make_entity(text, start, end, label):
    return EntitySpan(text=text, start=start, end=end, label=label)

def test_misalignment_policy_skip():
    tokens = [make_token(1, "Hello", 0, 5)]
    entities = [make_entity( "World", 6, 11, "MISC")]  # No token overlaps

    labeler = BIOLabeler(misalignment_policy="skip")
    labels = labeler.label(tokens, entities)
    assert labels == ["O"]


def test_misalignment_policy_warn(caplog):
    tokens = [make_token(1, "Hello", 0, 5)]
    entities = [make_entity("World", 6, 11, "MISC")]

    labeler = BIOLabeler(misalignment_policy="warn")
    with caplog.at_level("WARNING"):
        labels = labeler.label(tokens, entities)
        assert "No tokens align with entity" in caplog.text
    assert labels == ["O"]


def test_misalignment_policy_fail():
    tokens = [make_token(1, "Hello", 0, 5)]
    entities = [make_entity("World", 6, 11, "MISC")]

    labeler = BIOLabeler(misalignment_policy="fail")
    with pytest.raises(ValueError, match="No tokens align with entity"):
        labeler.label(tokens, entities)


@pytest.fixture(scope="module")
def tokenizer():
    return AutoTokenizer.from_pretrained("bert-base-uncased")

def test_bio_labeler_with_real_tokenizer_first(tokenizer):
    text = "Microsoft launched a new product."
    # Entity span for "Microsoft"
    entities = [EntitySpan(text="Microsoft", start=0, end=9, label="ORG")]

    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    offsets = encoding["offset_mapping"]
    tokens = [
        Token(id=input_id, text=tokenizer.convert_ids_to_tokens([input_id])[0], start=start, end=end)
        for input_id, (start, end) in zip(encoding["input_ids"], offsets)
    ]

    labeler = BIOLabeler(subword_strategy="first")
    labels = labeler.label(tokens, entities)

    assert labels[0].startswith("B-") or labels[0] == "O"
    assert labels.count("B-ORG") == 1
    assert labels.count("I-ORG") == 0

def test_bio_labeler_with_real_tokenizer_all(tokenizer):
    text = "Barack Obama visited Berlin."
    entities = [EntitySpan(text="Barack Obama", start=0, end=12, label="PER")]

    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = [
        Token(id=input_id, text=tokenizer.convert_ids_to_tokens([input_id])[0], start=start, end=end)
        for input_id, (start, end) in zip(encoding["input_ids"], encoding["offset_mapping"])
    ]

    labeler = BIOLabeler(subword_strategy="all")
    labels = labeler.label(tokens, entities)

    assert labels.count("B-PER") == 1
    assert "I-PER" in labels


@pytest.mark.parametrize("model_name", [
    "bert-base-uncased",        # WordPiece
    "roberta-base",             # BPE
    "albert-base-v2",           # SentencePiece
    "xlm-roberta-base",         # SPM+BPE
])
def test_bio_labeler_multitoken_entity_on_various_tokenizers(model_name):
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

    labeler = BIOLabeler(subword_strategy="all")
    labels = labeler.label(tokens, [entity])
    entity_labels = [label for label in labels if label != "O"]

    if len(entity_labels) == 1:
        assert entity_labels[0] == "B-PER"
    else:
        assert entity_labels[0] == "B-PER"
        for l in entity_labels[1:]:
            assert l == "I-PER"