# Getting Started

Welcome to **Chisel** — a lightweight and extensible Python library for preparing token-level annotation datasets for tasks like Named Entity Recognition (NER), Span Classification, and beyond.

Chisel tries to make it easy for NLP practitioners to experiment with different models when doing their extraction tasks by standardising the preprocessing steps and validation - making it easy to swap out models with different data and preprocessing requirements without spending ages on writing ad-hoc code.

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
| **Chunker**   | Optionally breaks long documents into chunks to fit token windows |
| **SpanAligner**   | Maps character spans to tokens |
| **Labeler**   | Converts token-level alignment into BIO, BILOU, or binary tags |
| **ParseValidator** | Ensures consistency between text and character spans|
| **TokenValidator** | Ensures consistency between character spans, tokens and labels  |
| **Formatters**  | Turns the final processed data to your preferred format |

Each component follows a defined Protocol, so you can swap in custom implementations as needed.

## 🚀 Examples
For examples as to how to use Chisel in pracice with common data annotations such as html tags, conll format or json, take a look at the notebooks in the example folder.


## 🚧 Development roadmap (in no particular order)
- Implement exporters for a broad range of data providers such as HuggingFaces Datasets, Pytorch Data, Spacy and DVC
- Implement parsers for common annotation tools such as Doccano, LabelStudio etc.
- Ensure compatibility with modern tokenizers such as BPE.
- Implement more sophisticated chunking methods for models with smaller token limits (like DistilBert 512)
- Design a principled and declarative way to build pipelines.

📖 What's Next?

- Learn how each [component works](components/parsers.md)
- Check out real-world examples
- Explore reference docs
