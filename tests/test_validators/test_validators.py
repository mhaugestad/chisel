import pytest
from typing import List
from transformers import AutoTokenizer
from chisel.extraction.models.models import Token, EntitySpan, TokenEntitySpan
from chisel.extraction.validators.validators import DefaultParseValidator, HFTokenAlignmentValidator, LabelSchemaValidator

def make_tokens(text: str, tokenizer_name: str = "bert-base-uncased") -> List[Token]:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    encoding = tokenizer(text, return_offsets_mapping=True)
    tokens = []
    for i, (start, end) in enumerate(encoding["offset_mapping"]):
        if start == end:
            continue
        token_text = text[start:end]
        tokens.append(Token(text=token_text, id=encoding["input_ids"][i], start=start, end=end))
    return tokens


def test_validators():
    sample_text = "Barack Obama was the president of the United States."
    entity_spans = [EntitySpan(text="Barack Obama", start=0, end=12, label="PER")]
    token_entity_spans = [TokenEntitySpan(entity=entity_spans[0], token_indices=[0, 1])]
    tokens = make_tokens(sample_text)
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    labels = ["O", "B-PER", "L-PER"] + ["O"] * (len(tokens) - 3)

    # Run all validators
    DefaultParseValidator().validate(sample_text, entity_spans)
    HFTokenAlignmentValidator(tokenizer).validate(tokens, token_entity_spans)


@pytest.mark.parametrize("on_error", ["warn", "raise"])
def test_label_schema_validator(capsys, on_error):
    allowed_labels = {"O", "PER", "ORG"}
    validator = LabelSchemaValidator(allowed_labels, on_error=on_error)

    # Valid case
    entity_spans = [EntitySpan(text="Barack Obama", start=0, end=12, label="PER")]
    validator.validate("Barack Obama was the president.", entity_spans)

    # Invalid case
    if on_error == "raise":
        entity_spans_invalid = [EntitySpan(text="Unknown Entity", start=0, end=15, label="UNKNOWN")]
        with pytest.raises(ValueError):
            validator.validate("Unknown Entity is not allowed.", entity_spans_invalid)

    elif on_error == "warn":
        entity_spans_invalid = [EntitySpan(text="Unknown Entity", start=0, end=15, label="UNKNOWN")]
        validator.validate("Unknown Entity is not allowed.", entity_spans_invalid)
        captured = capsys.readouterr()
        assert  "Warning: Entity label 'UNKNOWN' not in" in captured.out