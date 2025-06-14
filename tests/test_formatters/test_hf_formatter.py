# tests/test_formatters/test_hf_formatter.py
from chisel.extraction.models.models import ChiselRecord, Token, EntitySpan
from chisel.extraction.formatters.hf_formatter import HFDatasetFormatter


def test_hf_formatter_basic():
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
            bio_labels=["B-GREETING", "O"],
            labels=[0, 1],
        )
    ]

    formatter = HFDatasetFormatter()
    ds = formatter.format(records)

    assert len(ds) == 1
    row = ds[0]
    assert row["tokens"] == ["Hello", "world"]
    assert row["input_ids"] == [101, 102]
    assert row["attention_mask"] == [1, 1]
    assert row["labels"] == [0, 1]
    assert row["bio_labels"] == ["B-GREETING", "O"]
