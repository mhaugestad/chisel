# Chisel

Refining text. Shaping labels.
A modular and extensible preprocessing library for token classification tasks.

Chisel is a preprocessing library for token classification problems such as Named Entity Recognition (NER), Part-of-speech tagging, or custom span labelling tasks.

It turns raw annotated documents into model-ready datasets - handling tokenization, chunking, label alignment, validation and exporting following SOLID principles for maintainabiliyt and scalability.

Whether you are training a BERT model, fine-tuning a DistilBERT for NER or handling long sequence transformers, Chisel provides a flexible solution.


# Why Chisel?
Modern token classification tasks face common challenges.
* Mapping noisy or annotated text into structured labels (BIO, BILOU, ...)
* Handling tokenization artifacts (ie subwords, special characters)
* Dealing with model length limits
* Ensuring label alignment after chunking or splitting
* Building preprocessing pipelines that are modular, reusable and testable.

Chisel solves these problems by offering well-structured components that you can plug, swap or extend based on your needs.

# Key Features
* Modular Design
* Clean, extensible architecture
* Pluggable Components

# Installation
(Coming soon when packaging ready — or locally installable for now.)

```
git clone https://github.com/mhaugestad/chisel.git
cd chisel
pip install -e .
```

# Quick Start Example
See the examples folder for notebooks demonstrating how to use Chisel with common annotation formats.

# Project Principles
* Modularity: Components do one thing well
* Extensibility: Easy to plug in new logic (e.g., new chunker strategies)
* Testability: Core functionality is covered by unit and integration tests
* Transparency: Minimal hidden "magic" — explicit behavior

# 🛣 Roadmap

## 🔜 Short-Term Goals

- 🔧 Improve and extend existing components to support a broader range of annotation formats (e.g., HTML, XML, JSON), use cases and cover edge cases.

- ✨ Add support for multilabel tasks (i.e. overlapping spans).

- 📦 Implement exporters to support common data versioning and packaging frameworks (e.g., HuggingFace Datasets, DVC, PyTorch Dataset, etc).

- 🧠 Add spaCy compatibility (e.g., custom tokenizers, DocBin export, entity span management).

## 🚀 Long-Term Vision
🌐 Expand to additional neural NLP preprocessing tasks, such as:

- Graph-based representations (e.g., for GNNs).

- Entity linking and disambiguation.

- Relationship extraction and coreference resolution.

- Extractive Q and A

- ⚙️ Build plug-and-play components for end-to-end information extraction pipelines.


# Contributing
Contributions are welcome!

* Fork the repo
* Create a feature branch
* Do some coding.
* Make sure to pass the pre-commit
* Make sure to pass the unit test suites and implement tests on any new features developed
* Open a pull request with clear description and tests

Please strive to ensure your code adheres to the existing modular structure and follows SOLID principles.
