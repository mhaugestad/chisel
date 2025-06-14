# tests/test_formatters/test_torch_formatter.py
import pytest
from chisel.extraction.models.models import ChiselRecord, Token, EntitySpan
from chisel.extraction.formatters.torch_formatter import TorchDatasetFormatter

def test_torch_formatter_basic():
    records = [
        ChiselRecord(
            id="1",
            chunk_id=0,
            text="Hello world",
            tokens=[
                Token(id=101, text="Hello", start=0, end=5),
                Token(id=102, text="world", start=6, end=11)
            ],
            entities=[
                EntitySpan(text="Hello", start=0, end=5, label="GREETING"),
            ],
            input_ids=[101, 102],
            attention_mask=[1, 1],
            labels=[0, 1],
        )
    ]

    formatter = TorchDatasetFormatter()
    dataset = formatter.format(records)

    assert len(dataset) == 1
    item = dataset[0]
    assert item["input_ids"].tolist() == [101, 102]
    assert item["attention_mask"].tolist() == [1, 1]
    assert item["labels"].tolist() == [0, 1]
