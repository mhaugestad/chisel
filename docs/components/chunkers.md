# 🔪 Chunkers

Chunkers control how long texts are broken into smaller segments (chunks) for token classification tasks.

This is useful when:
- A document is too long for the model’s input length.
- You want to process text in overlapping windows.
- You need to preserve entity and token alignment across segments.

---

## 🧩 Chunker Protocols

Chisel supports two kinds of chunkers:

### 1. `TokenChunker`
Used when tokenization is already performed before chunking.

```python
class TokenChunker(Protocol):
    def chunk(self, tokens: List[Token], entities: List[TokenEntitySpan]) -> Tuple[List[List[Token]], List[List[TokenEntitySpan]]]:
        ...
```

Returns a tuple with a list of lists of Token objects and a list of lists of TokenEntitySpan objects:

- "tokens": the list of Token objects in the chunk.

- "entities": the list of EntitySpans that fall within the chunk.

### 2. TextChunker
Used to chunk text before tokenization.

```
class TextChunker(Protocol):
    def chunk(self, text: str, entities: List[EntitySpan]) -> Tuple[List[List[str]], List[List[EntitySpan]]]:
        ...
```

This is useful for early preprocessing stages or non-token-based chunking.

## 🧱 Built-in Chunkers
### NoOpChunker
Does not chunk. Returns the full document as a single chunk.

```
from chisel.chunkers import NoOpChunker

chunker = NoOpChunker()
chunks = chunker.chunk(tokens, entities)
```

### FixedLengthChunker
Splits tokens into non-overlapping fixed-size chunks.

```
from chisel.chunkers import FixedLengthChunker

chunker = FixedLengthChunker(chunk_size=128)
chunks = chunker.chunk(tokens, entities)
```
Entities that do not fully fit within the chunk are excluded.


## ⚙️ Notes on Entity Alignment
Chunkers are responsible for excluding entities that cross chunk boundaries.

This ensures downstream labelers do not mislabel partial entities.

## 🛠️ Custom Chunkers
You can implement your own chunking strategy by subclassing or following the TokenChunker/TextChunker protocol.

Example:

```
class SentenceChunker:
    def chunk(self, tokens, entities):
        # Group tokens into sentences using punctuation rules
        ...
```