# chisel/extraction/formatters/torch_formatter.py
from typing import List, Dict, Any
from torch.utils.data import Dataset
import torch
from chisel.extraction.models.models import ChiselRecord


class TorchNERDataset(Dataset):
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class TorchDatasetFormatter:
    """
    Converts a list of ChiselRecord instances into a PyTorch Dataset for training.

    Fields included:
    - input_ids
    - attention_mask
    - labels
    """

    def format(self, records: List[ChiselRecord]) -> Dataset:
        formatted = []
        for record in records:
            item = {
                "input_ids": torch.tensor(record.input_ids, dtype=torch.long),
                "attention_mask": torch.tensor(record.attention_mask, dtype=torch.long),
                "labels": torch.tensor(record.labels, dtype=torch.long),
            }
            formatted.append(item)
        return TorchNERDataset(formatted)
