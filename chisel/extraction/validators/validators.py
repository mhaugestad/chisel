from chisel.extraction.models.models import EntitySpan, Token, TokenEntitySpan
from chisel.extraction.base.protocols import (
    ParseValidator,
    TokenAlignmentValidator,
)
from transformers import PreTrainedTokenizerBase
from typing import Literal


class DefaultParseValidator(ParseValidator):
    """
    Default implementation that performs basic validation on entity spans:
    - Checks if entity text exists in the full text.
    - Checks if `entity.text` matches `text[start:end]`.
    - Checks for valid index boundaries.
    """

    def __init__(self, on_error: Literal["warn", "raise"] = "warn"):
        self.on_error = on_error

    def validate(self, text: str, span: EntitySpan) -> None:
        if not span.text:
            if self.on_error == "warn":
                print(f"Warning: Empty span text found at {span.start}-{span.end}")
            else:
                raise ValueError(f"Empty span text found at {span.start}-{span.end}")
        if not (0 <= span.start < span.end <= len(text)):
            if self.on_error == "warn":
                print(
                    f"Warning: Invalid span indices {span.start}-{span.end} for text length {len(text)}"
                )
            else:
                raise ValueError(
                    f"Invalid span indices: {span.start}-{span.end} for text length {len(text)}"
                )
        if span.text not in text:
            if self.on_error == "warn":
                print(f"Warning: Span text '{span.text}' not found in full text.")
            else:
                raise ValueError(f"Span text '{span.text}' not found in full text.")
        if text[span.start : span.end] != span.text:
            if self.on_error == "warn":
                print(
                    f"Warning: Span text mismatch at {span.start}-{span.end}: "
                    f"expected '{span.text}', found '{text[span.start:span.end]}'"
                )
            else:
                raise ValueError(
                    f"Span text mismatch: expected '{span.text}', found '{text[span.start:span.end]}'"
                )


class LabelSchemaValidator(ParseValidator):
    """
    Validates that all entity spans conform to a predefined label schema.
    """

    def __init__(
        self, allowed_labels: set[str], on_error: Literal["warn", "raise"] = "warn"
    ):
        self.allowed_labels = allowed_labels
        self.on_error = on_error

    def validate(self, text: str, span: EntitySpan) -> None:
        if span.label not in self.allowed_labels:
            if self.on_error == "warn":
                print(
                    f"Warning: Entity label '{span.label}' not in allowed labels {self.allowed_labels}."
                )
            else:
                raise ValueError(
                    f"Entity label '{span.label}' not in allowed labels {self.allowed_labels}."
                )


class HFTokenAlignmentValidator(TokenAlignmentValidator):
    """
    Validates that the tokens within each TokenEntitySpan, when decoded using
    the provided tokenizer, match the original entity text.
    """

    def __init__(
        self,
        tokenizer: PreTrainedTokenizerBase,
        on_error: Literal["warn", "raise"] = "warn",
    ):
        self.tokenizer = tokenizer
        self.on_error = on_error

    def validate(
        self,
        tokens: list[Token],
        span: TokenEntitySpan,
    ) -> None:
        # 1. Tokenize and decode the expected text
        encoded_expected = self.tokenizer(span.entity.text, add_special_tokens=False)
        decoded_expected = self.tokenizer.decode(encoded_expected["input_ids"]).strip()
        decoded_expected = decoded_expected.replace("##", "").strip()
        decoded_expected = decoded_expected.replace("Ġ", "").strip()

        # 2. Reconstruct the token ids from the original token list
        token_ids = [tokens[i].id for i in span.token_indices]
        decoded_actual = self.tokenizer.decode(token_ids).strip()
        decoded_actual = decoded_actual.replace("##", "").strip()
        decoded_actual = decoded_actual.replace("Ġ", "").strip()

        # 3. Compare
        if decoded_expected != decoded_actual:
            if self.on_error == "warn":
                print(
                    f"Warning: Token span and entity span mismatch:\n"
                    f"  Decoded actual: '{decoded_actual}'\n"
                    f"  Decoded expected: '{decoded_expected}'"
                )
            else:
                raise ValueError(
                    f"Token span and entity span mismatch:\n"
                    f"  Decoded actual: '{decoded_actual}'\n"
                    f"  Decoded expected: '{decoded_expected}'"
                )
