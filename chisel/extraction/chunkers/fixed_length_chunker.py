from typing import List, Tuple
from chisel.extraction.models.models import Token, TokenEntitySpan


# Implement the fixed-length chunker
class FixedLengthTokenChunker:
    def __init__(self, max_tokens: int = 256, overlap: int = 0):
        self.max_tokens = max_tokens
        self.overlap = overlap

    def chunk(
        self, tokens: List[Token], entities: List[TokenEntitySpan]
    ) -> Tuple[List[List[Token]], List[List[TokenEntitySpan]]]:
        chunks_tokens = []
        chunks_entities = []
        i = 0
        stride = self.max_tokens - self.overlap

        while i < len(tokens):
            token_chunk = tokens[i : i + self.max_tokens]

            # Stop if the chunk would be too small (e.g. last chunk has only 1 token)
            if len(token_chunk) < self.overlap and i != 0:
                break

            token_start = token_chunk[0].start

            # Filter and shift TokenEntitySpans
            chunk_entities = []
            for e in entities:
                if all(i <= idx < i + self.max_tokens for idx in e.token_indices):
                    shifted_indices = [idx - i for idx in e.token_indices]
                    shifted_entity = e.entity.copy(
                        update={
                            "start": e.entity.start - token_start,
                            "end": e.entity.end - token_start,
                        }
                    )
                    chunk_entities.append(
                        TokenEntitySpan(
                            entity=shifted_entity, token_indices=shifted_indices
                        )
                    )

            # Shift tokens
            shifted_tokens = [
                Token(
                    id=t.id,
                    text=t.text,
                    start=t.start - token_start,
                    end=t.end - token_start,
                )
                for t in token_chunk
            ]

            chunks_tokens.append(shifted_tokens)
            chunks_entities.append(chunk_entities)

            i += stride

        return chunks_tokens, chunks_entities
