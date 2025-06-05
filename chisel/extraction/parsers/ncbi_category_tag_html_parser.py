import re
from typing import List, Tuple
from chisel.extraction.models.models import EntitySpan
from chisel.extraction.base.protocols import Parser


class NCBICategoryTagHTMLParser(Parser):
    """
    A minimal HTML parser that extracts only `<category="LABEL">...</category>` spans.

    - Label is taken from the `category` attribute.
    - Text is cleaned of tags.
    """

    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        pattern = re.compile(r'<category="(.*?)">(.*?)</category>', re.DOTALL)
        spans = []
        cleaned = ""
        last_index = 0

        for match in pattern.finditer(doc):
            label, span_text = match.groups()
            start_tag_idx, end_tag_idx = match.span()

            # Append text between last tag and current one
            before = doc[last_index:start_tag_idx].strip()
            cleaned += before

            # Compute start and end char offsets in the cleaned string
            span_start = len(cleaned)
            cleaned += span_text
            span_end = len(cleaned)

            spans.append(
                EntitySpan(text=span_text, start=span_start, end=span_end, label=label)
            )
            last_index = end_tag_idx

        # Append remainder of text
        cleaned += doc[last_index:]

        return cleaned, spans
