# 🔄 Formatters
Formatters in Chisel convert `ChiselRecord` objects into the final data formats expected by downstream NLP model training libraries such as PyTorch and HuggingFace 🤗 Datasets.

They provide a clean separation between data processing and model consumption, making it easy to switch between libraries or pipelines.

## ✅ Supported Formatters
### `TorchDatasetFormatter`
Converts a list of `ChiselRecord` instances into a PyTorch-compatible dataset.

Output: `List[Dict[str, torch.Tensor]]`

Fields Included:

- `input_ids`

- `attention_mask`

- `labels`

Each record is represented as a dictionary where values are PyTorch tensors, ready to be wrapped in a `DataLoader`.

```
from chisel.extraction.formatters.torch_formatter import TorchDatasetFormatter

formatter = TorchDatasetFormatter()
torch_data = formatter.format(chisel_records)
```

### HFDatasetFormatter
Converts a list of `ChiselRecord` instances into a 🤗 HuggingFace `Dataset`.

Output: `datasets.Dataset` object

Fields Included:
- id
- chunk_id
- text
- input_ids
- attention_mask
- labels
- Optionally: bio_labels if present

Usage:
```
from chisel.extraction.formatters.hf_formatter import HFDatasetFormatter

formatter = HFDatasetFormatter()
hf_dataset = formatter.format(chisel_records)
```

## 🧩 Why Formatters?
Machine learning frameworks expect specific formats — not domain-rich objects like ChiselRecord. Formatters handle this final transformation step, letting you:

- Stay library-agnostic during preprocessing.

- Plug in different downstream toolkits easily.

- Avoid writing custom conversion logic repeatedly.