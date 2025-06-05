from pydantic import BaseModel, Field
from typing import List, Optional


class Token(BaseModel):
    id: int
    text: str
    start: int
    end: int


class EntitySpan(BaseModel):
    text: str
    start: int
    end: int
    label: str
    attributes: dict[str, str] = {}


class TokenEntitySpan(BaseModel):
    entity: EntitySpan
    token_indices: List[int]


class ChiselRecord(BaseModel):
    """
    A standardized representation of a processed data row in Chisel.

    This object serves as the internal format for exporting to different formats
    like HuggingFace Datasets, spaCy DocBin, or others.

    Required:
    - id: Unique identifier for the source document.
    - chunk_id: Unique chunk number for segmented inputs.
    - text: The original or cleaned text for this chunk.
    - tokens: List of Token objects.
    - entities: List of extracted EntitySpan objects.

    Optional:
    - bio_labels: List of BIO-style string labels.
    - labels: List of numeric labels (encoded version of bio_labels).
    - input_ids: Tokenizer-specific IDs for model input.
    - attention_mask: Attention mask corresponding to input_ids.
    """

    id: str
    chunk_id: int
    text: str
    tokens: List[Token]
    entities: List[EntitySpan]

    bio_labels: Optional[List[str]] = Field(default=None, alias="bio-labels")
    labels: Optional[List[int]] = None
    input_ids: Optional[List[int]] = None
    attention_mask: Optional[List[int]] = None
