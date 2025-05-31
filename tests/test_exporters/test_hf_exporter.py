import os
from datasets import load_from_disk
from chisel.extraction.exporters.hf_exporter import HuggingFaceExporter


def test_hf_exporter_saves_dataset(tmp_path):
    data = [
        {"id": "1", "tokens": ["Obama"], "labels": ["B-PER"]},
        {"id": "2", "tokens": ["UNICEF"], "labels": ["B-ORG"]},
    ]

    output_dir = tmp_path / "datasets"
    exporter = HuggingFaceExporter(output_dir=str(output_dir), dataset_name="my_ds")
    exporter.export(data)

    # Load it back
    loaded = load_from_disk(str(output_dir / "my_ds"))

    assert isinstance(loaded, list) or len(loaded) == 2
    assert loaded[0]["tokens"] == ["Obama"]
    assert loaded[1]["labels"] == ["B-ORG"]
