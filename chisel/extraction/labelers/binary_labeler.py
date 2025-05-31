from chisel.extraction.base.protocols import Labeler
from chisel.extraction.models.models import Token, EntitySpan
from typing import List, Literal
import logging

logger = logging.getLogger(__name__)


class BinaryLabeler(Labeler):
    """
    A labeler that converts character-based entity spans into binary labels aligned with tokenized text.

    Binary labels are produced with the following scheme:
    - ENTITY: Indicates a token that is part of an entity
    - O: Indicates a token that is outside any entity

    Parameters:
    ----------
    subword_strategy : {'first', 'all', 'strict'}, default='all'
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
        subword_strategy: Literal["first", "all", "strict"] = "first",
        misalignment_policy: Literal["skip", "warn", "fail"] = "skip",
    ):
        self.subword_strategy = subword_strategy
        self.misalignment_policy = misalignment_policy

    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        """
        Convert entity spans into binary labels aligned with tokenized text.
        Args:
            tokens (List[Token]): List of tokens with start and end offsets.
            entities (List[EntitySpan]): List of entity spans to label.
        Returns:
            List[str]: A list of binary labels corresponding to each token.
        """
        labels = ["O"] * len(tokens)

        for entity in entities:
            aligned = [
                (i, token)
                for i, token in enumerate(tokens)
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
                raise ValueError(
                    f"Unsupported subword strategy: {self.subword_strategy}"
                )

        return labels
