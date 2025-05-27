from chisel.base.protocols import Labeler
from chisel.models.models import Token, EntitySpan
from typing import List
import logging

logger = logging.getLogger(__name__)

class BinaryLabeler(Labeler):
    def __init__(self, subword_strategy: str = "first", misalignment_policy: str = "skip"):
        self.subword_strategy = subword_strategy
        self.misalignment_policy = misalignment_policy

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        labels = ["O"] * len(tokens)

        for entity in entities:
            aligned = [
                (i, token) for i, token in enumerate(tokens)
                if token.start >= entity.start and token.end <= entity.end
            ]

            if not aligned:
                if self.misalignment_policy == "fail":
                    raise ValueError(f"No tokens align with entity span: {entity}")
                elif self.misalignment_policy == "warn":
                    logger.warning(f"No tokens align with entity span: {entity}")
                continue

            token_indices = [i for i, _ in aligned]

            if self.subword_strategy == "first":
                labels[token_indices[0]] = "ENTITY"
            elif self.subword_strategy == "all":
                for i in token_indices:
                    labels[i] = "ENTITY"
            elif self.subword_strategy == "strict":
                # only label if entity span aligns exactly to token boundaries
                token_start = aligned[0][1].start
                token_end = aligned[-1][1].end
                if token_start == entity.start and token_end == entity.end:
                    for i in token_indices:
                        labels[i] = "ENTITY"
            else:
                raise ValueError(f"Unsupported subword strategy: {self.subword_strategy}")

        return labels
