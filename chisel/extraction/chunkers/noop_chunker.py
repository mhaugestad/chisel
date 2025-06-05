from typing import List, Tuple
from chisel.extraction.base.protocols import TokenChunker
from chisel.extraction.models.models import Token, TokenEntitySpan


class NoOpChunker(TokenChunker):
    def chunk(
        self, tokens: List[Token], token_entities: List[TokenEntitySpan]
    ) -> Tuple[List[List[Token]], List[List[TokenEntitySpan]]]:
        """
        No-op chunker that returns the input tokens and entities as a single chunk.
        Args:
            tokens (List[Token]): List of tokens to be chunked.
            entities (List[EntitySpan]): List of entity spans associated with the tokens.
        Returns:
            List[Dict]: A list containing a single dictionary with all tokens and entities.
        """
        return [tokens], [token_entities]
