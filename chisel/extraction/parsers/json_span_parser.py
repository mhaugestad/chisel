# chisel/parsers/json_span_parser.py

from typing import Tuple, List
from chisel.extraction.base.protocols import Parser
from chisel.extraction.models.models import EntitySpan

import json

class JSONSpanParser(Parser):
    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        """
        Parse a JSON-formatted string into plain text and entity spans.

        The input JSON must contain:
        - "text": a string of the original text
        - "entities": a list of dicts with "start", "end", and "label"

        Parameters:
        ----------
        doc : str
            A JSON string representing a single document with character-level entity annotations.

        Returns:
        -------
        Tuple[str, List[EntitySpan]]
            The original text and a list of extracted entity spans.
        """
        data = json.loads(doc)
        text = data["text"]
        entities = [
            EntitySpan(
                text=text[e["start"]:e["end"]],
                start=e["start"],
                end=e["end"],
                label=e["label"],
            )
            for e in data.get("entities", [])
        ]
        return text, entities
