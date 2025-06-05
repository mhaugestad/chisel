# ✅ Validators

Validators are used to check the integrity of your annotated data throughout the preprocessing pipeline. They help catch misaligned spans, mismatches between tokens and text, and ensure your data is clean and model-ready.

---

## 🔍 Validator Interface

```python
class Validator(Protocol):
    def validate(self, text: str, tokens: List[Token], entities: List[EntitySpan], labels: List[str]) -> None:
        ...
```

- Validators raise errors (or log warnings) when data is inconsistent.

- Can be composed in lists and called per chunk in a pipeline.

## 🧰 Built-in Validators

### 1. TextPresenceValidator
Checks that each EntitySpan.text is found somewhere in the full input string.
Useful to catch broken parsing, encoding issues, or mislabeling.

### 2. TextAlignmentValidator
Ensures that for each entity, the text[start:end] slice of the full string matches the entity’s .text.

- ✅ EntitySpan(text="Joe", start=0, end=3) and text[0:3] == "Joe" → valid

- ❌ text[0:3] == "Joh" → error

### 3. TokenAlignmentValidator
Verifies that tokens with non-O labels, when stitched back together, reproduce the EntitySpan.text.

Supports:

- BIO format: finds contiguous B-I spans.

- BILOU format: verifies U, B-I-L correctness.

- Uses the tokenizer to decode token spans.


Example failure:
```
Entity: Barack Obama
Tokens: ['BarackObama']
Decoded token span: 'BarackObama'
Expected: 'Barack Obama'
→ Raises ValueError
```

## 🛠 Custom Validators
You can create your own validator by implementing the Validator protocol:

```
class NoDuplicateEntitiesValidator:
    def validate(self, text, tokens, entities, labels):
        seen = set()
        for span in entities:
            if (span.start, span.end) in seen:
                raise ValueError("Duplicate entity span found.")
            seen.add((span.start, span.end))
```

🧪 Example Use
```
validators = [
    TextPresenceValidator(),
    TextAlignmentValidator(),
    TokenAlignmentValidator(tokenizer=my_tokenizer),
]
```

Used in pipelines like:

```
for validator in validators:
    validator.validate(text, tokens, entities, labels)
```

Next up: 📤 [Exporters](components/exporters.md) →