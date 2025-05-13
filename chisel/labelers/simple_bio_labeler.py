from typing import List
from chisel.base.protocols import Labeler
from chisel.models.models import Token, EntitySpan


class SimpleBIOLabeler(Labeler):
    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        labels = ["O"] * len(tokens)
        for entity in entities:
            for idx, token in enumerate(tokens):
                if token.start >= entity.start and token.end <= entity.end:
                    prefix = "B" if token.start == entity.start else "I"
                    labels[idx] = f"{prefix}-{entity.label}"
        return labels