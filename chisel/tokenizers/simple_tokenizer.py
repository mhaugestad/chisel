from typing import List
from chisel.base.protocols import Tokenizer
from chisel.models.models import Token


class SimpleWhitespaceTokenizer(Tokenizer):
    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenizes the input text into a list of Token objects based on whitespace.
        Args:
            text (str): The input text to be tokenized.
        Returns:
            List[Token]: A list of Token objects, each containing the token text, start and end positions.
        """
        tokens = []
        position = 0
        for idx, word in enumerate(text.split()):
            start = text.index(word, position)
            end = start + len(word)
            tokens.append(Token(
                id=idx,
                text = word,
                start = start,
                end = end
            ))
            position = end
        return tokens