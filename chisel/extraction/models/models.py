from pydantic import BaseModel, model_validator
from typing_extensions import Self


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
    attributes: dict[str, str] = {}

    @model_validator(mode="after")
    def check_start_end(self) -> Self:
        if self.start > self.end:
            raise ValueError("Start index must be less than or equal to end index")
        return self
