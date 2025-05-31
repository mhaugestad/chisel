from typing import Protocol, List, Dict, Literal, Tuple
from chisel.extraction.models.models import Token, EntitySpan


class Loader(Protocol):
    """
    A protocol for loading raw annotated documents from disk or remote sources.

    Implementations should return a list of dictionaries representing individual samples,
    typically with fields like "text", "html", or "annotations".
    """

    def load(self, path: str) -> List[Dict]:
        pass


class Parser(Protocol):
    """
    A protocol for converting annotated documents into a plain text string and structured entity spans.

    Example use case: stripping HTML tags and extracting entities into start-end labeled spans.
    """

    def parse(self, doc: str) -> tuple[str, List[EntitySpan]]:
        pass


class Tokenizer(Protocol):
    """
    A protocol for converting raw text into a sequence of tokens with offsets and IDs.

    Tokens must include start and end character offsets to support entity alignment.
    """

    def tokenize(self, text: str) -> List[Token]:
        pass


class TokenChunker(Protocol):
    """
    A protocol for chunking sequences of tokens and entity spans into smaller, self-contained units.

    Useful for handling model input length constraints (e.g., max 512 tokens in BERT).
    """

    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]: ...


class TextChunker(Protocol):
    """
    A protocol for chunking raw text and aligned entity spans before tokenization.

    This is typically used in workflows where chunking should happen before tokenization
    (e.g., character-based sliding windows).
    """

    def chunk(
        self, text: str, entities: List[EntitySpan]
    ) -> List[Tuple[str, List[EntitySpan]]]: ...


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

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        pass


class Validator(Protocol):
    """
    A protocol for validating text, tokens, entity spans, and labels to ensure preprocessing integrity.

    Implementations may check alignment between spans and text, label validity, or token-label consistency.
    """

    def validate(
        self,
        text: str,
        tokens: List[Token],
        entities: List[EntitySpan],
        labels: List[str],
    ) -> None: ...


class Exporter(Protocol):
    """
    A protocol for exporting processed datasets to external formats or destinations.

    Examples include exporting to JSON, Hugging Face datasets, or cloud storage.
    """

    def export(self, data: List[Dict]) -> None:
        pass


class LabelEncoder(Protocol):
    def fit(self, label_lists: List[List[str]]) -> None:
        """Builds the label vocabulary from multiple BIO label sequences."""

    def encode(self, labels: List[str]) -> List[int]:
        """Converts a single list of BIO labels to integer IDs."""

    def decode(self, ids: List[int]) -> List[str]:
        """Converts a list of integer IDs back to string labels."""

    def label2id(self, label: str) -> int: ...
    def id2label(self, idx: int) -> str: ...
