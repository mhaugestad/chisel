from typing import List
from chisel.extraction.models.models import Token, TokenEntitySpan
from chisel.extraction.base.protocols import Labeler


class BILOLabeler(Labeler):
    """
    Assigns BILOU labels to tokens based on their alignment with entities.
    Expects token-aligned entity spans via TokenEntitySpan.

    - B: Beginning of a multi-token entity
    - I: Inside a multi-token entity
    - L: Last token of a multi-token entity
    - O: Outside any entity
    - U: Unit-length entity (only one token)
    """

    def label(
        self, tokens: List[Token], token_entity_spans: List[TokenEntitySpan]
    ) -> List[str]:
        labels = ["O"] * len(tokens)

        for span in token_entity_spans:
            indices = span.token_indices
            n = len(indices)

            if n == 1:
                labels[indices[0]] = f"U-{span.entity.label}"
            elif n >= 2:
                labels[indices[0]] = f"B-{span.entity.label}"
                for idx in indices[1:-1]:
                    labels[idx] = f"I-{span.entity.label}"
                labels[indices[-1]] = f"L-{span.entity.label}"
            else:
                raise ValueError(f"TokenEntitySpan with no token indices: {span}")

        return labels
