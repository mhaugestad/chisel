# 📤 Exporters

# ⚠️ NOTE: Only protocol implemented. Will implement exporters to persist data to huggingface, DVC, spacy format etc in future.

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