from typing import List
from chisel.base.protocols import Tokenizer
from chisel.models.models import Token
import spacy

class SpacyTokenizer:
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.nlp = spacy.load(model_name, disable=["ner", "parser", "tagger"])

    def tokenize(self, text: str) -> List[Token]:
        doc = self.nlp(text)
        return [
            Token(id=token.i, text=token.text, start=token.idx, end=token.idx + len(token))
            for token in doc
        ]