from typing import List
from chisel.base.protocols import Validator

class BIOValidator:
    def validate(self, tokens: List[str], labels: List[str]) -> bool:
        return len(tokens) == len(labels)
