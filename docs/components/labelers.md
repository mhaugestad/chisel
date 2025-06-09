# 🏷 Labelers

Labelers convert annotated `EntitySpan` objects into token-level labels, typically in the **BIO**, **BILOU**, or **Binary** formats, which are required for training token classification models (e.g., for NER).

---
## 🧱 Labeler Interface

```python
class Labeler(Protocol):
    subword_strategy: Literal["first", "all", "strict"] = "strict"
    misalignment_policy: Literal["skip", "warn", "fail"] = "skip"

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        ...
```

⚙️ Parameters



| Parameter             | Description                                                                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subword_strategy`    | How to label subword tokens:<br>• `"first"` = label first subword only<br>• `"all"` = label all subwords<br>• `"strict"` = label only if token exactly matches entity |
| `misalignment_policy` | How to handle tokens that don’t align with any entity:<br>• `"skip"` = ignore<br>• `"warn"` = log a warning<br>• `"fail"` = raise an error                            |


## 🧰 Built-in Labelers
### 1. BIOLabeler
Applies standard BIO tagging:

B-<label>: Beginning of entity

I-<label>: Inside entity

O: Outside any entity

### 2. BILOLabeler
Uses more expressive BILOU tagging:

B-<label>: Beginning

I-<label>: Inside

L-<label>: Last

O: Outside

U-<label>: Unit (single-token entity)

### 3. BinaryLabeler
Simplified format for binary tasks:

ENTITY: Any token part of a span

O: Outside

🧪 Example

```python
from chisel.labelers.bio import BIOLabeler

labeler = BIOLabeler(subword_strategy="first", misalignment_policy="warn")
labels = labeler.label(tokens, entities)
# ["B-PER", "I-PER", "O", "O", "B-ORG", "I-ORG"]
```

### ⚠️ Subword Behavior
Subword tokenization can fragment entities:

Input text: "Barack Obama"

Tokens: ["Bar", "##ack", "Obama"]

Depending on the subword_strategy:

"first" → ["B-PER", "I-PER", "O"]

"all" → ["B-PER", "I-PER", "I-PER"]

"strict" → will only label if one token covers the full span

### 🧠 Tips
BIO/BILOU output is compatible with most token classification models.

Use LabelEncoder to convert string labels to integer IDs.

For debugging span alignment, use TokenAlignmentValidator.


## 🔢 LabelEncoder

The SimpleLabelEncoder is a lightweight utility for converting between string-based labels (e.g. "B-PER", "O") and integer IDs required by most machine learning frameworks.

Unlike typical encoders, this version requires you to pass in the label mapping explicitly at initialization — making its behavior predictable and immutable.

### 🧰 Features
Requires an explicit label_to_id dictionary at initialization.

- Converts labels to IDs (encode) and vice versa (decode).

- Throws helpful errors if unknown labels or IDs are encountered.

- Can be used internally in export pipelines for Hugging Face and PyTorch compatibility.

### 🧪 Example
```
from chisel.extraction.labelers.label_encoder import SimpleLabelEncoder

# Define a label-to-id mapping
label_map = {
    "O": 0,
    "B-PER": 1,
    "I-PER": 2,
    "B-LOC": 3,
    "I-LOC": 4
}

encoder = SimpleLabelEncoder(label_to_id=label_map)

# Encode a list of labels
label_ids = encoder.encode(["B-PER", "I-PER", "O"])  # ➝ [1, 2, 0]

# Decode a list of label IDs
decoded = encoder.decode([1, 2, 0])  # ➝ ["B-PER", "I-PER", "O"]
```

### ⚠️ Error Handling
If you try to encode or decode unknown values, the encoder raises a clear error:

```
encoder.encode(["B-ORG"])  
# ValueError: Unknown label 'B-ORG' encountered during encoding.
```

### 📦 API Reference

| Method              | Description                                       |
| ------------------- | ------------------------------------------------- |
| `encode(labels)`    | Convert list of label strings to integer IDs      |
| `decode(ids)`       | Convert list of integer IDs back to label strings |
| `get_label_to_id()` | Return internal label → ID dictionary             |
| `get_id_to_label()` | Return internal ID → label dictionary             |
