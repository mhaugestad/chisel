# ✅ Validators
Validators in Chisel help catch inconsistencies early in the preprocessing pipeline. They are divided into two categories:

## 🔍 Parse Validators
Parse validators run before tokenization and ensure that the entity spans extracted by the parser are accurate with respect to the original text.

### 🧩 Protocol
```
@runtime_checkable
class ParseValidator(Protocol):
    on_error: Literal["warn", "raise"]

    def validate(self, text: str, entities: List[EntitySpan]) -> None: ...
```

### 🛠️ Implementation: `DefaultParseValidator`
```
class DefaultParseValidator(ParseValidator):
    """
    - Checks if entity text exists in the full text.
    - Checks if `entity.text` matches `text[start:end]`.
    - Checks for valid index boundaries.
    - Warns or raises on errors based on `on_error`.
    """
```

### 🔧 Behavior

| Check                            | Description                                  |
| -------------------------------- | -------------------------------------------- |
| `entity.text in text`            | Ensures the string exists in the input text. |
| `text[start:end] == entity.text` | Confirms character indices match the string. |
| `0 <= start < end <= len(text)`  | Validates index boundaries.                  |
| Empty `text`                     | Raises or warns on empty span texts.         |

### 💡 Usage
```
validator = DefaultParseValidator(on_error="raise")
validator.validate(text, entities)
```

## 🧷 Token Alignment Validators
These validators ensure that token-aligned entity spans can be reconstructed accurately from the token IDs using the tokenizer.

### 🧩 Protocol
```
@runtime_checkable
class TokenAlignmentValidator(Protocol):
    on_error: Literal["warn", "raise"]

    def validate(
        self, tokens: List[Token], token_entity_spans: List[TokenEntitySpan]
    ) -> None: ...
```

### 🛠️ Implementation: `HFTokenAlignmentValidator`
```
class HFTokenAlignmentValidator(TokenAlignmentValidator):
    """
    - Tokenizes `entity.text` and decodes it.
    - Compares to decoded token IDs from aligned tokens.
    - Warns or raises if mismatch is found.
    """
```

### 🔧 Behavior
| Check                       | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| Decode `entity.text`        | Using HuggingFace tokenizer (`add_special_tokens=False`). |
| Decode token span using IDs | From `TokenEntitySpan.token_indices`.                     |
| Compare decoded strings     | If mismatch, either warn or raise.                        |

### 💡 Usage

```
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

validator = HFTokenAlignmentValidator(tokenizer=tokenizer, on_error="warn")
validator.validate(tokens, token_entity_spans)
```
## ⚠️ on_error Behavior
All validators accept an on_error argument:

| Value     | Effect                                         |
| --------- | ---------------------------------------------- |
| `"raise"` | Raises an exception immediately (strict mode). |
| `"warn"`  | Logs a warning and continues execution.        |

This allows you to use strict checks during development, but run more flexibly during large-scale preprocessing.

## 🛠️ Implementing Custom Validators
You can easily extend Chisel by writing your own validator classes that follow the appropriate protocol.

### ✅ Custom `ParseValidator`
To write a custom validator that checks the parsed spans before tokenization, inherit from or implement the ParseValidator protocol:

```
from chisel.extraction.base.protocols import ParseValidator
from chisel.extraction.models import EntitySpan

class NoOverlappingSpansValidator(ParseValidator):
    """
    Ensures that no two entity spans overlap in character space.
    """

    def __init__(self, on_error: Literal["warn", "raise"] = "warn"):
        self.on_error = on_error

    def validate(self, text: str, entities: list[EntitySpan]) -> None:
        sorted_entities = sorted(entities, key=lambda e: e.start)
        for i in range(len(sorted_entities) - 1):
            if sorted_entities[i].end > sorted_entities[i + 1].start:
                msg = (
                    f"Overlapping spans: '{sorted_entities[i]}' "
                    f"and '{sorted_entities[i + 1]}'"
                )
                if self.on_error == "warn":
                    print("Warning:", msg)
                else:
                    raise ValueError(msg)
```

### ✅ Custom TokenAlignmentValidator
To write a validator that checks alignment between tokens and entities, use the TokenAlignmentValidator protocol:

```
from chisel.extraction.base.protocols import TokenAlignmentValidator
from chisel.extraction.models import Token, TokenEntitySpan

class NoEmptySpanValidator(TokenAlignmentValidator):
    """
    Ensures no TokenEntitySpan has zero token indices.
    """

    def __init__(self, on_error: Literal["warn", "raise"] = "warn"):
        self.on_error = on_error

    def validate(
        self,
        tokens: list[Token],
        token_entity_spans: list[TokenEntitySpan],
    ) -> None:
        for span in token_entity_spans:
            if not span.token_indices:
                msg = f"TokenEntitySpan for '{span.entity.text}' has no token indices."
                if self.on_error == "warn":
                    print("Warning:", msg)
                else:
                    raise ValueError(msg)
```

### 🧪 Tip: Chain Multiple Validators
You can combine multiple validators in your pipeline like so:
```
parse_validators = [
    DefaultParseValidator(on_error="raise"),
    NoOverlappingSpansValidator(on_error="warn"),
]

for validator in parse_validators:
    validator.validate(text, entities)
```

This design encourages small, composable units of validation logic.