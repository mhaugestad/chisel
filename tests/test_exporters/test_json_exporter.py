import json
import pytest
from chisel.extraction.exporters.json_exporter import JSONExporter

def test_json_exporter(tmp_path):
    data = [
        {"id": "1", "tokens": ["Barack", "Obama"], "labels": ["B-PER", "I-PER"]},
        {"id": "2", "tokens": ["UNICEF"], "labels": ["B-ORG"]}
    ]
    output_path = tmp_path / "output.json"

    exporter = JSONExporter(output_path=str(output_path))
    exporter.export(data)

    with open(output_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data
