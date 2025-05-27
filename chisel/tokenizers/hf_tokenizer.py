from typing import List
from chisel.base.protocols import Tokenizer
from chisel.models.models import Token
from transformers import AutoTokenizer

class HFTokenizer:
    def __init__(self, model_name: str = "bert-base-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(self, text: str) -> List[Token]:
        encoding = self.tokenizer(
            text,
            return_offsets_mapping=True,
            add_special_tokens=False,
            return_tensors=None
        )
        tokens = self.tokenizer.tokenize(text)

        return [
            Token(
                id=idx,
                text=tok, 
                start=start + 1 if tok.startswith("Ġ") else start, 
                end=end)
            for tok, idx, (start, end) in zip(tokens, encoding["input_ids"], encoding["offset_mapping"])
        ]
