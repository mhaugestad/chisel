import logging
from typing import List, Literal
from chisel.extraction.base.protocols import Labeler
from chisel.extraction.models.models import Token, EntitySpan

logger = logging.getLogger(__name__)


class BILOLabeler(Labeler):
    """
    A labeler that converts character-based entity spans into BILOU labels aligned with tokenized text.

    BILOU stands for:
    - B: Beginning of an entity
    - I: Inside an entity (not first or last)
    - L: Last token of an entity
    - O: Outside any entity
    - U: Unit token, used when a single token covers the entire entity

    Parameters:
    ----------
    subword_strategy : {'first', 'all', 'strict'}, default='strict'
        Strategy for handling entities that span multiple subword tokens:
        - 'first': Only label the first subword as B-, rest as I-, L-.
        - 'all': Label all subwords using B-, I-, L- or U- as appropriate.
        - 'strict': Only label tokens whose span exactly matches the entity. Others are skipped.

    misalignment_policy : {'skip', 'warn', 'fail'}, default='skip'
        Determines behavior when an entity cannot be aligned with any tokens:
        - 'skip': Silently skip the unmatched entity.
        - 'warn': Log a warning with entity details.
        - 'fail': Raise a ValueError indicating the mismatch.

    Returns:
    -------
    List[str]
        A list of BILOU-formatted labels, one for each input token.
    """

    def __init__(
        self,
        subword_strategy: Literal["first", "all", "strict"] = "all",
        misalignment_policy: Literal["skip", "warn", "fail"] = "skip",
    ):
        self.subword_strategy = subword_strategy
        self.misalignment_policy = misalignment_policy

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        """
        Convert entity spans into BILOU labels aligned with tokenized text.
        Args:
            tokens (List[Token]): List of tokens with start and end offsets.
            entities (List[EntitySpan]): List of entity spans to label.
        Returns:
            List[str]: A list of BILOU labels corresponding to each token.
        """
        labels = ["O"] * len(tokens)

        for entity in entities:
            matched_indices = [
                idx
                for idx, token in enumerate(tokens)
                if not (token.end <= entity.start or token.start >= entity.end)
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
                        labels[idx] = (
                            f"U-{entity.label}"  # Treat strict exact match as Unit
                        )
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
