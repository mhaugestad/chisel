import pytest
from chisel.parsers.html_tag_parser import HTMLTagParser
from chisel.models.models import EntitySpan

@pytest.mark.parametrize(
    "html_input, expected_text, expected_entities",
    [
        # Basic example
        (
            "The <ORG>UN</ORG> met with <PER>Joe Biden</PER> today.",
            "The UN met with Joe Biden today.",
            [
                EntitySpan(text="UN", start=4, end=6, label="ORG"),
                EntitySpan(text="Joe Biden", start=16, end=25, label="PER")
            ]
        ),
        # No entities
        (
            "This is a normal sentence.",
            "This is a normal sentence.",
            []
        ),
        # Entity at start
        (
            "<PER>Obama</PER> gave a speech.",
            "Obama gave a speech.",
            [EntitySpan(text="Obama", start=0, end=5, label="PER")]
        ),
        # Multiple same-type entities
        (
            "<ORG>UN</ORG> and <ORG>WHO</ORG> met.",
            "UN and WHO met.",
            [
                EntitySpan(text="UN", start=0, end=2, label="ORG"),
                EntitySpan(text="WHO", start=7, end=10, label="ORG")
            ]
        ),
        # Non-entity tag should be ignored
        (
            "This is <b>bold</b> and <PER>Jane</PER> is a person.",
            "This is bold and Jane is a person.",
            [EntitySpan(text="Jane", start=17, end=21, label="PER")]
        ),
    ]
)
def test_html_tag_parser_variants(html_parser, html_input, expected_text, expected_entities):
    text, entities = html_parser.parse(html_input)

    assert text == expected_text

    # Compare entity content (ignoring object identity)
    assert len(entities) == len(expected_entities)
    for actual, expected in zip(entities, expected_entities):
        assert actual.text == expected.text
        assert actual.start == expected.start
        assert actual.end == expected.end
        assert actual.label == expected.label
        assert expected_text[actual.start:actual.end] == actual.text
        assert expected_text[expected.start:expected.end] == expected.text


@pytest.mark.parametrize(
    "html_input, expected_text, expected_entities",
    [

        # Existing test (control)
        (
            "The <PER>UN</PER> met with <PER>Joe Biden</PER> today.",
            "The UN met with Joe Biden today.",
            [
                EntitySpan(text="UN", start=4, end=6, label="PER"),
                EntitySpan(text="Joe Biden", start=16, end=25, label="PER")
            ]
        ),

        # Attribute on entity tag
        (
            "<PER role=\"CEO\">Alice</PER> runs the company.",
            "Alice runs the company.",
            [
                EntitySpan(text="Alice", start=0, end=5, label="PER", attributes={"role": "CEO"})
            ]
        ),

        # Unknown tag (should be ignored)
        (
            "The <b>bold</b> word is <PER>Obama</PER>.",
            "The bold word is Obama.",
            [
                EntitySpan(text="Obama", start=17, end=22, label="PER")
            ]
        ),

        # Nested tag (flatten inner only)
        (
            "<ORG><PRODUCT>Google</PRODUCT></ORG> announced a launch.",
            "Google announced a launch.",
            [
                EntitySpan(text="Google", start=0, end=6, label="PRODUCT")
            ]
        ),

        # Broken tag (missing close)
        (
            "The CEO is <PER>Elon Musk and the CTO is <PER>Jane Doe</PER>.",
            "The CEO is Elon Musk and the CTO is Jane Doe.",
            [
                # Only Jane Doe gets labeled
                EntitySpan(text="Jane Doe", start=35, end=43, label="PER")
            ]
        ),

        # Domain-specific tag
        (
            "Refer to <STATUTE>Article 14</STATUTE> in <CASE>Smith v. Jones</CASE>.",
            "Refer to Article 14 in Smith v. Jones.",
            [
                EntitySpan(text="Article 14", start=9, end=19, label="STATUTE"),
                EntitySpan(text="Smith v. Jones", start=23, end=37, label="CASE")
            ]
        ),

    ]
)
def test_html_tag_parser_edge_cases(html_parser, html_input, expected_text, expected_entities):
    text, entities = html_parser.parse(html_input)

    assert text == expected_text

    assert len(entities) == len(expected_entities)
    for actual, expected in zip(entities, expected_entities):
        assert actual.text == expected.text
        assert actual.start == expected.start
        assert actual.end == expected.end
        assert actual.label == expected.label
        assert actual.attributes == expected.attributes


@pytest.mark.xfail
def test_malformed_entity_does_not_drop_text():
    html = "The CEO is <PER>Elon Musk and the CTO is <PER>Jane Doe</PER>."
    expected_text = "The CEO is Elon Musk and the CTO is Jane Doe."
    ...