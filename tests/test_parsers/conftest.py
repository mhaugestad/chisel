import pytest
from chisel.extraction.parsers.html_tag_parser import HTMLTagParser

@pytest.fixture
def html_parser():
    return HTMLTagParser()
