from typing import Protocol, List, Dict, Literal, Tuple
from chisel.models.models import Token, EntitySpan

class Loader(Protocol):
    def load(self, path: str) -> List[Dict]:
        pass

class Parser(Protocol):
    def parse(self, doc: str) -> tuple[str, List[EntitySpan]]:
        pass

class Tokenizer(Protocol):
    def tokenize(self, text: str) -> List[Token]:
        pass
    
class TokenChunker(Protocol):
    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]: ...

class TextChunker(Protocol):
    def chunk(self, text: str, entities: List[EntitySpan]) -> List[Tuple[str, List[EntitySpan]]]: ...
    
class Labeler(Protocol):
    subword_strategy: Literal["first", "all", "strict"] = "strict",
    misalignment_policy: Literal["skip", "warn", "fail"] = "skip"
    
    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        pass

class Validator(Protocol):
    def validate(self, text: str, tokens: List[Token], entities: List[EntitySpan], labels: List[str]) -> None:
        pass

class Exporter(Protocol):
    def export(self, data: List[Dict]) -> None:
        pass