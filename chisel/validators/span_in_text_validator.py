from typing import List
from chisel.models.models import Token, EntitySpan

class SpanInTextValidator:
    def validate(self, text: str, tokens, entities: List[EntitySpan], labels=None):
        for ent in entities:
            if ent.text not in text:
                raise ValueError(f"Span text '{ent.text}' not found in text.")
