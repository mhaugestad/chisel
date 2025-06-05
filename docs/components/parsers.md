# 🧩 Parsers

Parsers are the entry point to the Chisel pipeline. They take raw annotated documents and extract the **cleaned text** and a list of **entity spans** (`EntitySpan`) with their character offsets.

Each parser implements the following protocol:

```python
class Parser(Protocol):
    def parse(self, doc: str) -> tuple[str, List[EntitySpan]]:
        ...
```

## 🧱 Available Parsers
### 1. HTMLTagParser
Parses entity spans from non-standard HTML/XML tags like <PER>, <ORG>, or custom tags like <Entity type="person">.

🧪 Example Input
```html
The <ORG>UN</ORG> met with <PER>Joe Biden</PER> today.
```

✅ Output

Cleaned Text: `"The UN met with Joe Biden today."`

`EntitySpan(label="ORG", start=4, end=6, text="UN")`

`EntitySpan(label="PER", start=16, end=25, text="Joe Biden")`

🔧 Parameters

| Name             | Description                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| `label_strategy` | `"tag"` to use the tag name as label (e.g., `PER`) or `"attribute"` to extract a specific HTML attribute as the label |
| `attribute_name` | Used if `label_strategy="attribute"` — specifies which attribute to use as label                                      |
| `allow_nested`   | If `True`, allows nested tags and creates spans for each. If `False`, only outermost span is retained                 |


### 2. JSONSpanParser
Parses a dictionary with plain text and list of character-based annotations.

🧪 Example Input
```json
{
  "text": "Barack Obama was president.",
  "entities": [
    {"start": 0, "end": 12, "label": "PER"}
  ]
}
```

✅ Output

Cleaned Text: `"Barack Obama was president."`

`EntitySpan(label="PER", start=0, end=12, text="Barack Obama")`


### 3. ConllParser
Parses text in CoNLL format with token-level BIO or BILOU tags

🧪 Example Input
```
Tim B-PER
Cook I-PER
is O
the O
CEO O
of O
Apple B-ORG
. O
```

✅ Output

Cleaned Text: `"Tim Cook is the CEO of Apple."`

`EntitySpan(label="PER", start=0, end=8, text="Tim Cook")`

`EntitySpan(label="ORG", start=24, end=29, text="Apple")`

### 🧠 Notes
Parsers are intentionally minimal and decoupled from tokenization.

You can easily extend Chisel by writing your own parser, e.g., for PDFs, docx files, or domain-specific formats.

All parsers return spans using start/end character offsets on the cleaned version of the text.


### ➕ Custom Parsers
To implement your own parser, simply conform to the protocol:

```
class MyCustomParser:
    def parse(self, doc: str) -> tuple[str, List[EntitySpan]]:
        # 1. Extract raw text
        # 2. Identify annotated spans with start, end, label
        # 3. Return cleaned text and EntitySpan list
        ...
```