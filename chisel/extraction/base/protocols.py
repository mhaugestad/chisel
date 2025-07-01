from typing import Protocol, List, Dict, Literal, Tuple, Any, runtime_checkable
from chisel.extraction.models.models import (
    Token,
    EntitySpan,
    TokenEntitySpan,
    ChiselRecord,
)


@runtime_checkable
class Loader(Protocol):
    """
    A protocol for loading raw annotated documents from disk or remote sources.

    Implementations should return a list of dictionaries representing individual samples,
    typically with fields like "text", "html", or "annotations".
    """

    def load(self, path: str) -> List[Dict]:
        pass


@runtime_checkable
class Parser(Protocol):
    """
    A protocol for converting annotated documents into a plain text string and structured entity spans.

    Example use case: stripping HTML tags and extracting entities into start-end labeled spans.
    """

    def parse(self, doc: str) -> tuple[str, List[EntitySpan]]:
        pass


@runtime_checkable
class Tokenizer(Protocol):
    """
    A protocol for converting raw text into a sequence of tokens with offsets and IDs.

    Tokens must include start and end character offsets to support entity alignment.
    """

    def tokenize(self, text: str) -> List[Token]:
        pass


@runtime_checkable
class TokenChunker(Protocol):
    """
    A protocol for chunking sequences of tokens and aligned token entity spans into smaller, self-contained units.

    Useful for handling model input length constraints (e.g., max 512 tokens in BERT).
    """

    def chunk(
        self, tokens: List[Token], entities: List[TokenEntitySpan]
    ) -> Tuple[List[List[Token]], List[List[TokenEntitySpan]]]: ...


@runtime_checkable
class TextChunker(Protocol):
    """
    A protocol for chunking raw text and aligned entity spans before tokenization.

    This is typically used in workflows where chunking should happen before tokenization
    (e.g., character-based sliding windows).
    """

    def chunk(
        self, text: str, entities: List[EntitySpan]
    ) -> List[Tuple[str, List[EntitySpan]]]: ...


class SpanAligner(Protocol):
    """
    A protocol for aligning entity spans with tokenized text.

    This is necessary because tokenization can split words into subwords, and entities
    may not align perfectly with the resulting tokens.
    """

    def align(
        self, tokens: List[Token], entities: List[EntitySpan]
    ) -> List[TokenEntitySpan]: ...


@runtime_checkable
class Labeler(Protocol):
    """
    A protocol for converting entity spans into token-level labels using a labeling scheme like BIO or BILOU.

    Supports subword-aware strategies and misalignment handling.

    Parameters:
        subword_strategy: Determines how subword tokens are labeled. Options:
            - "first": label only the first subword token
            - "all": label all subword tokens
            - "strict": label only when the span matches exactly one token

        misalignment_policy: Determines how to handle entity spans that do not align cleanly with tokens.
            - "skip": ignore these spans
            - "warn": log a warning
            - "fail": raise an error
    """

    subword_strategy: Literal["first", "all", "strict"] = "strict"
    misalignment_policy: Literal["skip", "warn", "fail"] = "skip"

    def label(
        self, tokens: List[Token], token_entity_spans: List[TokenEntitySpan]
    ) -> List[str]:
        """
        Assigns labels (e.g. BIO, BILOU) to a sequence of tokens using pre-aligned TokenEntitySpan objects.
        """
        ...


@runtime_checkable
class ParseValidator(Protocol):
    """
    A protocol for validating a single parsed entity span before tokenization.

    Responsibilities may include:
    - Ensuring the `text` in each `EntitySpan` exists verbatim in the input `text`.
    - Ensuring character start and end indices are valid and consistent with the span text.
    - Detecting malformed or overlapping spans.

    Inputs:
        text (str): The full input string after parsing.
        entities (List[EntitySpan]): The list of extracted spans from the parser.
    """

    on_error: Literal["warn", "raise"]

    def validate(self, text: str, entity: EntitySpan) -> None: ...


@runtime_checkable
class TokenAlignmentValidator(Protocol):
    """
    A protocol for validating that token-level alignments of entities are correct.

    This is meant to ensure that the tokens corresponding to an entity span,
    when decoded using the tokenizer, match the original text span.

    Inputs:
        tokens (List[Token]): Tokenized representation of the text.
        token_entity_spans (List[TokenEntitySpan]): Entity spans with associated token indices.
    """

    on_error: Literal["warn", "raise"]

    def validate(
        self, tokens: List[Token], token_entity_span: TokenEntitySpan
    ) -> None: ...


@runtime_checkable
class LabelAlignmentValidator(Protocol):
    """
    A protocol for validating that the output label sequence is consistent with entity spans.

    This validator reconstructs spans from the label sequence (e.g., using BIO or BILOU)
    and compares them to the expected token entity spans.

    Inputs:
        tokens (List[Token]): Tokenized representation of the text.
        labels (List[str]): Label sequence assigned to each token.
        token_entity_spans (List[TokenEntitySpan]): Expected token spans representing entities.
    """

    def validate(
        self,
        tokens: List[Token],
        labels: List[str],
        token_entity_spans: List[TokenEntitySpan],
    ) -> None: ...


@runtime_checkable
class DatasetFormatter(Protocol):
    def format(self, records: List[ChiselRecord]) -> Any: ...


@runtime_checkable
class Exporter(Protocol):
    """
    A protocol for exporting processed datasets to external formats or destinations.

    Examples include exporting to JSON, Hugging Face datasets, or cloud storage.
    """

    def export(self, data: List[ChiselRecord]) -> None:
        pass


@runtime_checkable
class LabelEncoder(Protocol):
    """
    A protocol for encoding and decoding string-based labels into integer format,
    suitable for training classification models.

    This encoder must be fitted before use.
    """

    def encode(self, labels: List[str]) -> List[int]:
        """Encodes a single list of string labels into integer labels."""
        ...

    def decode(self, ids: List[int]) -> List[str]:
        """Decodes a list of integers back into string labels."""
        ...

    def get_label_to_id(self) -> dict:
        """Returns the label-to-ID mapping."""
        ...

    def get_id_to_label(self) -> dict:
        """Returns the ID-to-label mapping."""
        ...
