# chisel/extraction/formatters/hf_formatter.py
from typing import List, Dict, Any
from datasets import Dataset
from chisel.extraction.models.models import ChiselRecord


class HFDatasetFormatter:
    """
    Converts ChiselRecord instances into a Hugging Face `datasets.Dataset`.

    Output fields:
    - id: str
    - chunk_id: int
    - tokens: List[str]
    - input_ids: List[int]
    - attention_mask: List[int]
    - labels: List[int]
    - bio_labels: List[str] (if available)
    """

    def format(self, records: List[ChiselRecord]) -> Dataset:
        rows: List[Dict[str, Any]] = []
        for record in records:
            rows.append(
                {
                    "id": record.id,
                    "chunk_id": record.chunk_id,
                    "tokens": [t.text for t in record.tokens],
                    "input_ids": record.input_ids,
                    "attention_mask": record.attention_mask,
                    "labels": record.labels,
                    "bio_labels": record.bio_labels,
                }
            )
        return Dataset.from_list(rows)
