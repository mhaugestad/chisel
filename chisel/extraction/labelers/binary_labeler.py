from typing import List
from chisel.extraction.models.models import Token, TokenEntitySpan
from chisel.extraction.base.protocols import Labeler


class BinaryLabeler(Labeler):
    """
    Assigns binary labels to tokens based on their presence in any entity span.

    - ENTITY: For any token inside a labeled span, regardless of its label type
    - O: Outside any entity

    This is useful for training models that perform binary token classification.
    """

    def label(
        self, tokens: List[Token], token_entity_spans: List[TokenEntitySpan]
    ) -> List[str]:
        labels = ["O"] * len(tokens)

        for span in token_entity_spans:
            for idx in span.token_indices:
                labels[idx] = "ENTITY"

        return labels
