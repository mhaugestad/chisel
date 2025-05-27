import logging
from typing import List, Literal
from chisel.base.protocols import Labeler
from chisel.models.models import Token, EntitySpan

logger = logging.getLogger(__name__)

class BILOLabeler(Labeler):
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
                continue

            n = len(matched_indices)

            if self.subword_strategy == "strict":
                for idx in matched_indices:
                    token = tokens[idx]
                    if token.start == entity.start and token.end == entity.end:
                        labels[idx] = f"U-{entity.label}"  # Treat strict exact match as Unit
                continue

            if self.subword_strategy == "first":
                if n == 1:
                    labels[matched_indices[0]] = f"U-{entity.label}"
                else:
                    labels[matched_indices[0]] = f"B-{entity.label}"
                    labels[matched_indices[-1]] = f"L-{entity.label}"
                    for mid_idx in matched_indices[1:-1]:
                        labels[mid_idx] = f"I-{entity.label}"

            elif self.subword_strategy == "all":
                if n == 1:
                    labels[matched_indices[0]] = f"U-{entity.label}"
                else:
                    for i, idx in enumerate(matched_indices):
                        if i == 0:
                            labels[idx] = f"B-{entity.label}"
                        elif i == n - 1:
                            labels[idx] = f"L-{entity.label}"
                        else:
                            labels[idx] = f"I-{entity.label}"

        return labels
