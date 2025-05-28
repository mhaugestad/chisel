import pytest
from chisel.parsers.archived_html_tag_parser import HTMLTagParser

@pytest.fixture
def html_parser():
    return HTMLTagParser()
