# ✂️ Tokenizers

Tokenizers split raw text into smaller units (tokens) and assign each token:
- The **text** (string form of the token)
- The **start** and **end** character offsets in the original text
- The **token ID** (usually the vocabulary index from a model tokenizer)

Chisel uses tokenizers to align character-level entity spans with model-compatible tokens for tasks like Named Entity Recognition (NER).

---

## 🧱 Tokenizer Interface

Each tokenizer implements the following protocol:

```python
class Tokenizer(Protocol):
    def tokenize(self, text: str) -> List[Token]:
        ...
```

Where Token is:

```python
class Token(BaseModel):
    id: int       # model vocab ID
    text: str     # token string
    start: int    # start char index
    end: int      # end char index
```

## 🧰 Built-in Tokenizers
### 1. HuggingFaceTokenizer

Wraps any pretrained Hugging Face tokenizer (AutoTokenizer) and outputs properly aligned Token objects.

🔧 Parameters
| Name       | Description                                                                 |
| ---------- | --------------------------------------------------------------------------- |
| `model_id` | Pretrained model name (e.g., `"bert-base-uncased"`, `"distilroberta-base"`) |

🧪 Example
```python
from chisel.tokenizers.hf_tokenizer import HuggingFaceTokenizer

tokenizer = HuggingFaceTokenizer("bert-base-uncased")
tokens = tokenizer.tokenize("Barack Obama was president.")
```
Returns a list of Token objects with offsets and token IDs.

## ⚠️ Tokenizer Behavior
Different tokenizers use different subword strategies:

WordPiece (e.g., BERT): breaks unknown words into fragments with ## prefix

BPE (e.g., RoBERTa, GPT2): breaks based on byte-pair frequencies, often splits tokens at character level

SentencePiece (e.g., ALBERT, T5): learned segmentation of raw text with special prefix tokens like ▁

These affect how span alignment and labeling must be handled. Chisel supports multiple subword alignment strategies (see [Labelers](components/labelers.md)) to accommodate this.


## 🧠 Tips
Use tokenizer.tokenize() when creating datasets or debugging span alignment.

The returned tokens are automatically compatible with labelers and chunkers.

You can test tokenizer behavior on edge cases using the tests/test_tokenizers suite.

## ➕ Custom Tokenizer
To create your own tokenizer, simply implement the protocol:

```
class MyCustomTokenizer:
    def tokenize(self, text: str) -> List[Token]:
        # Custom logic
        ...

```

Next up: 🏷 [Labelers](components/labelers.md) →