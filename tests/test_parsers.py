import pytest
from chisel.parsers.html_tag_parser import HTMLTagParser

@pytest.fixture
def html():
    return "The <ORG>UN</ORG> met with <PER>Joe Biden</PER> today."

def test_import(html):
    parser = HTMLTagParser()
    text, entities = parser.parse(html)
    assert text == "The UN met with Joe Biden today."
    assert len(entities) == 2
    assert entities[0].text == "UN"
    assert entities[0].start == 4
    assert entities[0].end == 6
    assert entities[0].label == "ORG"
    assert entities[1].text == "Joe Biden"
    assert entities[1].start == 16
    assert entities[1].end == 25
    assert entities[1].label == "PER"