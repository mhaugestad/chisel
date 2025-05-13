from pydantic import BaseModel, model_validator
from typing_extensions import Self
from typing import List

class Token(BaseModel):
    id: int
    text: str
    start: int
    end: int

class EntitySpan(BaseModel):
    text: str
    start: int
    end: int
    label: str

    @model_validator(mode='after')
    def check_start_end(self) -> Self:
        if self.start > self.end:
            raise ValueError("Start index must be less than or equal to end index")
        return self
    
class Chunk(BaseModel):
    text: str
    tokens: List[Token]
    entities: List[EntitySpan]
    chunk_id: int

    @model_validator(mode='after')
    def check_text(self) -> Self:
        for entity in self.entities:
            if entity.text not in self.text:
                raise ValueError(f"Entity text '{entity.text}' not found in chunk text")
        return self
    
    @model_validator(mode='after')
    def check_span(self) -> Self:
        for entity in self.entities:
            if self.text != self.text[entity.start:entity.end]:
                raise ValueError("Entity span does not match text: {entity.text} != {self.text[entity.start:entity.end]}")
        return self
    
class Document(BaseModel):
    id: str
    chunks: List[Chunk]