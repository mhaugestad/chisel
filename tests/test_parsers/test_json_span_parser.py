# tests/test_parsers/test_json_span_parser.py

import pytest
from chisel.extraction.parsers.json_span_parser import JSONSpanParser
from chisel.extraction.models.models import EntitySpan


def test_json_span_parser_basic():
    parser = JSONSpanParser()
    json_str = """
    {
        "text": "Tim Cook is the CEO of Apple.",
        "entities": [
            {"start": 0, "end": 8, "label": "PER"},
            {"start": 23, "end": 28, "label": "ORG"}
        ]
    }
    """
    text, spans = parser.parse(json_str)

    assert text == "Tim Cook is the CEO of Apple."
    assert len(spans) == 2
    assert spans[0] == EntitySpan(text="Tim Cook", start=0, end=8, label="PER")
    assert spans[1] == EntitySpan(text="Apple", start=23, end=28, label="ORG")
