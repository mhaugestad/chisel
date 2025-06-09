# 🧱 Data Models in Chisel
Chisel uses a small set of clearly defined, Pydantic-based data models to standardize the representation of annotated texts, tokenization outputs, and aligned spans. These models form the internal "data language" that parsers, tokenizers, labelers, and exporters operate on.

## 📍 Token

Represents a single token within a text, along with its character-level span.

```
class Token(BaseModel):
    id: int
    text: str
    start: int
    end: int
```

| Field   | Type  | Description                                     |
| ------- | ----- | ----------------------------------------------- |
| `id`    | `int` | Unique identifier (usually index in token list) |
| `text`  | `str` | Raw token text                                  |
| `start` | `int` | Character start index in the original text      |
| `end`   | `int` | Character end index (exclusive)                 |


Example:

```json
{
  "id": 0,
  "text": "aspirin",
  "start": 0,
  "end": 7
}
```

## 🧠 EntitySpan
Represents a labeled span of text extracted from annotations, often prior to tokenization.
```
class EntitySpan(BaseModel):
    text: str
    start: int
    end: int
    label: str
    attributes: dict[str, str] = {}
```

| Field        | Type   | Description                                |
| ------------ | ------ | ------------------------------------------ |
| `text`       | `str`  | The extracted text span                    |
| `start`      | `int`  | Start character index                      |
| `end`        | `int`  | End character index (exclusive)            |
| `label`      | `str`  | The entity label (e.g. "DISEASE", "ORG")   |
| `attributes` | `dict` | Optional metadata associated with the span |


## 🔗 TokenEntitySpan
Aligns an EntitySpan to its token-level representation. Used after tokenization and alignment.
```
class TokenEntitySpan(BaseModel):
    entity: EntitySpan
    token_indices: List[int]
```

| Field           | Type         | Description                                             |
| --------------- | ------------ | ------------------------------------------------------- |
| `entity`        | `EntitySpan` | The original span                                       |
| `token_indices` | `List[int]`  | Indices into the `Token` list that align with this span |

This format is useful for converting between span-level and sequence-label formats like BIO/BILOU.

## 🧾 ChiselRecord
A central container for all relevant information about a processed text segment. Used throughout pipelines and by all exporters.

```
class ChiselRecord(BaseModel):
    id: str
    chunk_id: int
    text: str
    tokens: List[Token]
    entities: List[EntitySpan]
    bio_labels: Optional[List[str]] = Field(default=None, alias="bio-labels")
    labels: Optional[List[int]] = None
    input_ids: Optional[List[int]] = None
    attention_mask: Optional[List[int]] = None
```

| Field            | Type                  | Description                                 |
| ---------------- | --------------------- | ------------------------------------------- |
| `id`             | `str`                 | Unique document ID                          |
| `chunk_id`       | `int`                 | Unique ID for this chunk of the document    |
| `text`           | `str`                 | The original or preprocessed text           |
| `tokens`         | `List[Token]`         | Tokenized representation of the text        |
| `entities`       | `List[EntitySpan]`    | Extracted entities in character span format |
| `bio_labels`     | `Optional[List[str]]` | BIO/BILOU labels (one per token)            |
| `labels`         | `Optional[List[int]]` | Encoded integer labels                      |
| `input_ids`      | `Optional[List[int]]` | Tokenizer output for transformer input      |
| `attention_mask` | `Optional[List[int]]` | Attention mask corresponding to input\_ids  |

Example:
```
{
  "id": "doc123",
  "chunk_id": 0,
  "text": "Aspirin is used to treat pain.",
  "tokens": [...],
  "entities": [...],
  "bio_labels": ["B-DRUG", "O", "O", "O", "O"],
  "labels": [1, 0, 0, 0, 0],
  "input_ids": [101, 1234, 2003, ...],
  "attention_mask": [1, 1, 1, ...]
}
```
