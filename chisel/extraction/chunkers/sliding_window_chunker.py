from typing import List, Dict
from chisel.extraction.models.models import Token, EntitySpan

class SlidingWindowChunker:
    def __init__(self, window_size: int = 512, stride: int = 256):
        """Initializes the SlidingWindowChunker with a specified window size and stride.
        Args:
            window_size (int): Size of the sliding window in characters.
            stride (int): Number of characters to move the window for each chunk.
        """

        self.window_size = window_size
        self.stride = stride

    def chunk(self, text: str, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]:
        """Chunks the provided text into overlapping segments using a sliding window approach.
        Args:
            text (str): The full text to be chunked.
            tokens (List[Token]): List of tokens to be associated with the text.
            entities (List[EntitySpan]): List of entity spans associated with the text.
        Returns:
            List[Dict]: A list of dictionaries, each containing a chunk of text, tokens, and entities.
        """
        chunks = []
        text_length = len(text)

        for offset in range(0, text_length, self.stride):
            window_start = offset
            window_end = min(offset + self.window_size, text_length)
            chunk_text = text[window_start:window_end]

            # Select tokens that fall fully inside the window
            chunk_tokens = [
                Token(
                    id=token.id,
                    text=token.text,
                    start=token.start - window_start,
                    end=token.end - window_start
                )
                for token in tokens
                if token.start >= window_start and token.end <= window_end
            ]

            # Select and offset entities
            chunk_entities = [
                EntitySpan(
                    text=ent.text,
                    start=ent.start - window_start,
                    end=ent.end - window_start,
                    label=ent.label,
                    attributes=ent.attributes,
                )
                for ent in entities
                if ent.start >= window_start and ent.end <= window_end
            ]

            chunks.append({
                "text": chunk_text,
                "tokens": chunk_tokens,
                "entities": chunk_entities,
                "offset": window_start
            })

        return chunks
