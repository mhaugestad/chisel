# Getting Started

Welcome to **Chisel** — a lightweight and extensible Python library for preparing token-level annotation datasets for tasks like Named Entity Recognition (NER), Span Classification, and beyond.

This guide will walk you through setting up Chisel, understanding the core concepts, and running your first processing pipeline.

---

## 🧰 Installation

```bash
pip install -e .  # From source
```

Ensure you have a compatible Python version (3.8–3.11 recommended) and install dependencies:

```bash
pip install -r requirements.txt
```


## 🧱 Core Concepts
Chisel follows a modular pipeline architecture with pluggable components:

| Component     | Role                                                           |
| ------------- | -------------------------------------------------------------- |
| **Parser**    | Extracts raw entity spans from annotated documents             |
| **Tokenizer** | Splits raw text into tokens                                    |
| **Chunker**   | Optionally breaks long documents into chunks                   |
| **Labeler**   | Converts token-level alignment into BIO, BILOU, or binary tags |
| **Validator** | Ensures consistency between text, spans, and labels            |
| **Exporter**  | Saves the final processed data to your preferred format        |

Each component follows a defined Protocol, so you can swap in custom implementations as needed.

🚀 Quickstart Example

Here’s a minimal example to get you started:

```bash
from chisel.extraction.parsers import HTMLTagParser
from chisel.extraction.tokenizers import HFTokenizer
from chisel.extraction.labelers import BIOLabeler
from chisel.extraction.chunkers import NoOpChunker
from chisel.extraction.validators import SpanTextMatchValidator
from chisel.extraction.exporters import JSONExporter
from chisel.extraction.models import EntitySpan
from chisel.extraction.labelers import SimpleLabelEncoder

# Your input
doc = "The <ORG>UN</ORG> met with <PER>Joe Biden</PER> today."

# Setup pipeline
parser = HTMLTagParser(label_strategy="tag")
tokenizer = HFTokenizer("bert-base-uncased")
chunker = NoOpChunker()
labeler = BIOLabeler(subword_strategy="first", misalignment_policy="warn")
label_encoder = SimpleLabelEncoder()
validator = SpanTextMatchValidator()
exporter = JSONExporter(output_path="output.json")

# Run
text, spans = parser.parse(doc)
tokens = tokenizer.tokenize(text)
chunks = chunker.chunk(tokens, spans)
labels = [labeler.label(chunk["tokens"], chunk["entities"]) for chunk in chunks]
label_encoder.fit(labels)
encoded = [label_encoder.encode(lbl) for lbl in labels]

for chunk, lbl in zip(chunks, labels):
    validator.validate(text, chunk["tokens"], chunk["entities"], lbl)

exporter.export([
    {
        "text": text,
        "tokens": [t.text for t in tokens],
        "labels": labels[0],
        "encoded_labels": encoded[0],
    }
])
```

📖 What's Next?

- Learn how each [component works](components/parsers.md)
- Check out real-world examples
- Explore reference docs

