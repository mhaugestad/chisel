from chisel.extraction.parsers.html_tag_parser import HTMLTagParser
from chisel.extraction.models.models import EntitySpan


def test_parse_with_tag_label_strategy():
    parser = HTMLTagParser(label_strategy="tag")
    html = "The <person>CEO</person> spoke."
    text, spans = parser.parse(html)

    assert text == "The CEO spoke."
    assert len(spans) == 1
    assert spans[0].label == "PERSON"
    assert spans[0].text == "CEO"
    assert spans[0].start == 4
    assert spans[0].end == 7
    assert text == "The CEO spoke."


def test_parse_with_attribute_label_strategy():
    parser = HTMLTagParser(label_strategy="attribute", attribute_name="type")
    html = "The <entity type='ORG'>Google</entity> announced a launch."
    text, spans = parser.parse(html)

    assert text == "The Google announced a launch."
    assert len(spans) == 1
    assert spans[0].label == "ORG"
    assert spans[0].text == "Google"
    assert spans[0].start == 4
    assert spans[0].end == 10
    assert spans[0].attributes["type"] == "ORG"
    assert text == "The Google announced a launch."


def test_parse_excludes_standard_tags():
    parser = HTMLTagParser(label_strategy="tag")
    html = "<p>The <person>CEO</person> spoke.</p>"
    text, spans = parser.parse(html)

    assert text == "The CEO spoke."
    assert len(spans) == 1
    assert spans[0].label == "PERSON"


def test_parse_nested_tags_allow_nested():
    parser = HTMLTagParser(label_strategy="tag", allow_nested=True)
    html = "The <role><person>CEO</person></role> spoke."
    text, spans = parser.parse(html)

    assert text == "The CEO spoke."
    assert len(spans) == 2

    labels = sorted(
        [(s.label, s.start, s.end, s.text) for s in spans], key=lambda x: x[0]
    )
    assert labels[0] == ("PERSON", 4, 7, "CEO")
    assert labels[1] == ("ROLE", 4, 7, "CEO")


def test_parse_nested_tags_without_allow_nested():
    parser = HTMLTagParser(label_strategy="tag", allow_nested=False)
    html = "The <role><person>CEO</person></role> spoke."
    text, spans = parser.parse(html)

    assert text == "The CEO spoke."
    assert len(spans) == 1
    assert spans[0].label == "ROLE"
    assert spans[0].text == "CEO"
    assert spans[0].start == 4
    assert spans[0].end == 7


def test_parse_custom_tags():
    parser = HTMLTagParser(label_strategy="tag", allow_nested=False)
    html = "The <ORG>UN</ORG> met with <PER>Joe Biden</PER> today."
    text, spans = parser.parse(html)
    assert text == "The UN met with Joe Biden today."
    assert len(spans) == 2
    assert spans[0].label == "ORG"
    assert spans[0].text == "UN"
    assert spans[0].start == 4
    assert spans[0].end == 6
