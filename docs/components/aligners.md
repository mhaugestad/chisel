# 🧩 Aligners
Aligners are responsible for mapping annotated character-based entity spans onto their corresponding token indices after tokenization. This step is crucial for generating label sequences in BIO, BILOU, or binary tagging formats.

## ✅ Responsibilities
Take in a list of Token objects and a list of EntitySpan objects.

Return a list of TokenEntitySpan objects, which attach each entity to the indices of the tokens that represent it.

Ensure accurate alignment even when tokenization introduces splitting (e.g., subwords from BPE tokenizers).

## 🛠 Interfaces
TokenAligner Protocol
```
class TokenAligner(Protocol):
    def align(self, tokens: List[Token], entities: List[EntitySpan]) -> List[TokenEntitySpan]:
        ...
```
This protocol defines the expected interface for all aligners.

## 🚀 Implementations

### HuggingfaceTokenAligner
An alignment strategy designed for Huggingface-style tokenizers. It works by:

- Matching token character spans with entity spans.

- Mapping each entity to the smallest contiguous list of token indices that fully cover its span.

- Optionally normalizing whitespace and punctuation to improve matching robustness.

#### Output
- Each aligner returns a list of TokenEntitySpan objects:

```python
TokenEntitySpan(
    entity=EntitySpan(
        text="Barack Obama",
        start=0,
        end=12,
        label="PER"
    ),
    token_indices=[0, 1]
)
```
## 🔎 Validation
Aligners should be paired with validators (like ValidateLabelAlignment) to ensure that the token spans can accurately reconstruct the original entity text after tokenization. This helps catch tokenizer mismatches or annotation inconsistencies.

## 📚 Example Usage
```
tokens = tokenizer.tokenize("Barack Obama visited the USA.")
entities = [EntitySpan(text="Barack Obama", start=0, end=12, label="PER")]

aligned = aligner.align(tokens, entities)

# Produces token indices covering the span "Barack Obama"
```