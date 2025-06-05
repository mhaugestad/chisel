# 📤 Exporters

Exporters define how the final, processed data is saved, serialized, or made available to downstream tasks like model training or data inspection.

Chisel comes with built-in exporters for common formats, and you can also implement your own.

---

## 🧩 Exporter Interface

```python
class Exporter(Protocol):
    def export(self, data: List[Dict]) -> None:
        ...
```

- data: A list of processed data samples.

- Each sample is typically a dictionary with fields like input_ids, labels, tokens, etc.

- Exporters are typically used at the end of a pipeline.



## 📦 Built-in Exporters

### 1. JSONExporter
Saves the full dataset to a single .json or .jsonl file.

```
from chisel.exporters import JSONExporter

exporter = JSONExporter(output_path="outputs/data.json", jsonl=True)
exporter.export(data)
```

Options:

- jsonl=True: Save one example per line (JSON Lines format).

- jsonl=False: Save entire dataset as one JSON array.

### 2. HFDatasetExporter
Exports to a 🤗 Hugging Face Dataset format, optionally saving to disk.

```
from chisel.exporters import HFDatasetExporter

exporter = HFDatasetExporter(path="outputs/hf-dataset", split="train")
exporter.export(data)
```

- Converts list of dicts into a datasets.Dataset.

- Optionally saves to disk or returns in-memory object.

## 🧠 Custom Exporters
You can easily write your own exporter by implementing the protocol:

```
class CSVExporter:
    def __init__(self, output_path):
        self.output_path = output_path

    def export(self, data: List[Dict]) -> None:
        import csv
        with open(self.output_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
```

## 💡 Best Practices
Keep exporters format-agnostic—don’t assume specific label formats.

Use label_encoder.inverse_transform(...) if you want to write human-readable labels.

Consider whether you need to split your data (e.g., into train/val/test) before exporting.