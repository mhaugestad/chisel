from typing import List, Dict
from chisel.base.protocols import Chunker
from chisel.models.models import Token, EntitySpan


class NoOpChunker(Chunker):
    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]:
        return [
            {
                "tokens": tokens,
                "entities": entities,
                "chunk_id": 0
             }
        ]