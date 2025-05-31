# Chisel

Refining text. Shaping labels.
A modular and extensible preprocessing library for token classification tasks.

Chisel is a prprocessing library for token classification problems such as Named Entity Recognition (NER), Part-of-speech tagging, or custom span labelling tasks.

It turns raw annotated documents into model-ready datasets - handling tokenization, chunking, label alignment, validation and exporting following SOLID principles for maintainabiliyt and scalability.

Whether you are training a BERT model, fine-tuning a DistilBERT for NER or handling long sequence transformers, Chisel provides a flexible solution.


# Why Chisel?
Modern token classification tasks face common challenges.
* Mapping noisy or annotated text into structured BIO labels
* Handling tokenization artifacts (ie subwords, special characters)
* Dealing with model length limits
* Ensuring label alignment after chunking or splitting
* Building preprocessing pipelines that are modular, reusable and testable.

Chisel solves these problems by offering well-structured components that you can plug, swap or extend based on your needs.

# Key Features
* Modular Design: Loader → Parser → Tokenizer → Chunker → Labeler → Validator → Exporter
* SOLID Principles: Clean, extensible architecture
* BIO Label Handling: Automatic BIO encoding from spans
* Long Sequence Support: Sliding window chunker and sentence-based chunker
* Typed Data Models: Pydantic-backed, schema-validated classes
* Pluggable Components: Easy to add custom tokenizers, chunkers, or labelers
* Configurable Pipelines: YAML/JSON based pipeline configs
* Friendly Logging: Consistent, minimal logging throughout the pipeline

# Installation
(Coming soon when packaging ready — or locally installable for now.)

```
git clone https://github.com/yourname/chisel.git
cd chisel
pip install -e .
```

# Quick Start Example
```
from chisel import PreprocessingPipeline
from chisel.loaders import JSONHTMLLoader
from chisel.parsers import HTMLTagParser
from chisel.tokenizers import HFTokenizer
from chisel.chunkers import SlidingWindowChunker
from chisel.labelers import SimpleBIOLabeler
from chisel.validators import BIOValidator
from chisel.exporters import JSONExporter
from chisel.schemas import LabelSchema

schema = LabelSchema(labels=["O", "B-PER", "I-PER", "B-ORG", "I-ORG"])

pipeline = PreprocessingPipeline(
    loader=JSONHTMLLoader(),
    parser=HTMLTagParser(),
    tokenizer=HFTokenizer(model_name="bert-base-cased"),
    chunker=SlidingWindowChunker(max_length=512, stride=128),
    labeler=SimpleBIOLabeler(schema=schema),
    validator=BIOValidator(schema=schema),
    exporter=JSONExporter()
)

pipeline.run("data/input.json", "data/output.json")
```

# Project Principles
* Modularity: Components do one thing well
* Extensibility: Easy to plug in new logic (e.g., new chunker strategies)
* Testability: Core functionality is covered by unit and integration tests
* Transparency: Minimal hidden "magic" — explicit behavior

Roadmap
- [] Core preprocessing pipeline

- [] Sliding window chunker

- [] Sentence-based chunker

- [] Augmentation framework

- [] CLI runner for pipelines

- [] HuggingFace Dataset export integration

- [] Streamlit or Gradio visualization tools (future)


# Contributing
Contributions are welcome!

* Fork the repo
* Create a feature branch
* Open a pull request with clear description and tests

Please ensure your code adheres to the existing modular structure and follows SOLID principles.

# License
(Define later — probably MIT, Apache 2.0, or similar.)
