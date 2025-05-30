from typing import List, Dict
from chisel.models.models import Token, EntitySpan

class FixedLengthChunker:
    def __init__(self, max_tokens: int = 256, overlap: int = 0):
        """Initializes the FixedLengthChunker with a maximum token length and overlap.
        Args:
            max_tokens (int): Maximum number of tokens per chunk.
            overlap (int): Number of tokens to overlap between consecutive chunks.
        """
        self.max_tokens = max_tokens
        self.overlap = overlap

    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]:
        """Chunks the provided tokens and entities into fixed-length segments.
        Args:
            tokens (List[Token]): List of tokens to be chunked.
            entities (List[EntitySpan]): List of entity spans associated with the tokens.
        Returns:
            List[Dict]: A list of dictionaries, each containing a chunk of tokens and their associated entities.
        """
        chunks = []
        stride = self.max_tokens - self.overlap
        i = 0

        while i < len(tokens):
            token_chunk = tokens[i:i + self.max_tokens]
            token_start = token_chunk[0].start
            token_end = token_chunk[-1].end

            # Filter entities that fall fully inside this chunk
            chunk_entities = [
                EntitySpan(
                    text=e.text,
                    start=e.start - token_start,
                    end=e.end - token_start,
                    label=e.label,
                    attributes=e.attributes
                )
                for e in entities if token_start <= e.start and e.end <= token_end
            ]

            # Offset tokens to be chunk-relative
            chunk_tokens = [
                Token(
                    id=t.id,
                    text=t.text,
                    start=t.start - token_start,
                    end=t.end - token_start
                )
                for t in token_chunk
            ]

            chunks.append({
                "tokens": chunk_tokens,
                "entities": chunk_entities,
                "offset": i
            })

            i += stride

        return chunks
