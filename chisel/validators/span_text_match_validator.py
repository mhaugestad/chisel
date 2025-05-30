from typing import List
from chisel.models.models import EntitySpan

class SpanTextMatchValidator:
    def validate(self, text: str, tokens, entities: List[EntitySpan], labels=None):
        for ent in entities:
            expected = text[ent.start:ent.end]
            if ent.text != expected:
                raise ValueError(
                    f"Text mismatch for entity {ent.label} at ({ent.start}-{ent.end}): "
                    f"expected '{expected}', got '{ent.text}'"
                )