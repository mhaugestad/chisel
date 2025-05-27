from typing import Protocol, List, Dict
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
    
class Chunker(Protocol):
    def chunk(self, tokens: List[Token], entities: List[EntitySpan]) -> List[Dict]:
        pass
    
class Labeler(Protocol):
    def label(self, tokens: List[Token], entities: List[EntitySpan]) -> List[str]:
        pass

class Validator(Protocol):
    def validate(self, tokens: List[str], labels: List[str]) -> bool:
        pass

class Exporter(Protocol):
    def export(self, data: List[Dict]) -> None:
        pass