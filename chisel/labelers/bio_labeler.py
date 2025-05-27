import logging
from typing import List, Literal
from chisel.base.protocols import Labeler
from chisel.models.models import Token, EntitySpan

logger = logging.getLogger(__name__)

class BIOLabeler(Labeler):
    def __init__(
        self,
        subword_strategy: Literal["first", "all", "strict"] = "strict",
        misalignment_policy: Literal["skip", "warn", "fail"] = "skip"
    ):
        self.subword_strategy = subword_strategy
        self.misalignment_policy = misalignment_policy

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        labels = ["O"] * len(tokens)

        for entity in entities:
            matched_indices = [
                idx for idx, token in enumerate(tokens)
                if token.start >= entity.start and token.end <= entity.end
            ]

            if not matched_indices:
                message = f"No tokens align with entity span: {entity.text} ({entity.start}-{entity.end})"
                if self.misalignment_policy == "warn":
                    logger.warning(message)
                elif self.misalignment_policy == "fail":
                    raise ValueError(message)
                continue  # skip in all cases

            if self.subword_strategy == "strict":
                for idx in matched_indices:
                    token = tokens[idx]
                    if token.start == entity.start and token.end == entity.end:
                        labels[idx] = f"B-{entity.label}"
                continue

            if self.subword_strategy == "first":
                labels[matched_indices[0]] = f"B-{entity.label}"

            elif self.subword_strategy == "all":
                for i, idx in enumerate(matched_indices):
                    prefix = "B" if i == 0 else "I"
                    labels[idx] = f"{prefix}-{entity.label}"

        return labels
