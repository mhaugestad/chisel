from typing import List
from chisel.extraction.models.models import Token, EntitySpan, TokenEntitySpan


class TokenSpanAligner:
    """
    Aligns entity spans to tokens by finding which tokens fall within the character spans of the entities.
    This is useful for tasks like NER where entities need to be mapped to tokenized text.
    """

    def align(
        self, entities: List[EntitySpan], tokens: List[Token]
    ) -> List[TokenEntitySpan]:
        """
        For each EntitySpan, find the list of token indices that fall fully within its character span.
        Returns a list of TokenEntitySpan objects.
        """
        results = []
        for entity in entities:
            token_indices = [
                idx
                for idx, token in enumerate(tokens)
                if token.start >= entity.start and token.end <= entity.end
            ]
            results.append(TokenEntitySpan(entity=entity, token_indices=token_indices))
        return results
