import pytest
from chisel.extraction.parsers.conll_parser import ConllParser
from chisel.extraction.models.models import EntitySpan


def test_conll_parser_basic_bio():
    parser = ConllParser()

    doc = """Tim B-PER
Cook I-PER
is O
the O
CEO O
of O
Apple B-ORG
. O"""

    text, spans = parser.parse(doc)

    assert text == "Tim Cook is the CEO of Apple."
    assert spans == [
        EntitySpan(text="Tim Cook", start=0, end=8, label="PER"),
        EntitySpan(text="Apple", start=23, end=28, label="ORG"),
    ]
