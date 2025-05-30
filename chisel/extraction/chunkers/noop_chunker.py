from typing import List, Dict
from chisel.extraction.base.protocols import Chunker
from chisel.extraction.models.models import Token, EntitySpan


class NoOpChunker(Chunker):
    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]:
        """
        No-op chunker that returns the input tokens and entities as a single chunk.
        Args:
            tokens (List[Token]): List of tokens to be chunked.
            entities (List[EntitySpan]): List of entity spans associated with the tokens.
        Returns:
            List[Dict]: A list containing a single dictionary with all tokens and entities.
        """
        return [
            {
                "tokens": tokens,
                "entities": entities,
                "chunk_id": 0
             }
        ]