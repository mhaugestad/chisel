import logging
from typing import List, Literal
from chisel.extraction.base.protocols import Labeler
from chisel.extraction.models.models import Token, TokenEntitySpan

logger = logging.getLogger(__name__)


class BIOLabeler(Labeler):
    def __init__(
        self,
        subword_strategy: Literal["first", "all", "strict"] = "strict",
        misalignment_policy: Literal["skip", "warn", "fail"] = "skip",
    ):
        self.subword_strategy = subword_strategy
        self.misalignment_policy = misalignment_policy

    def label(
        self, tokens: List[Token], token_entity_spans: List[TokenEntitySpan]
    ) -> List[str]:
        labels = ["O"] * len(tokens)

        for span in token_entity_spans:
            indices = span.token_indices
            label = span.entity.label
            if not indices:
                message = f"No aligned tokens for entity: {span.entity}"
                if self.misalignment_policy == "warn":
                    logger.warning(message)
                elif self.misalignment_policy == "fail":
                    raise ValueError(message)
                continue

            if len(indices) == 1:
                labels[indices[0]] = f"B-{label}"
            else:
                labels[indices[0]] = f"B-{label}"
                for i in indices[1:]:
                    labels[i] = f"I-{label}"

        return labels
