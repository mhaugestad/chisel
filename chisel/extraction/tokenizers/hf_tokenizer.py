from typing import List
from chisel.extraction.models.models import Token
from transformers import AutoTokenizer


class HFTokenizer:
    def __init__(self, model_name: str = "bert-base-cased"):
        """Initializes the HFTokenizer with a specified model name.
        Args:
            model_name (str): Name of the pre-trained model to use for tokenization.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(self, text: str) -> List[Token]:
        """Tokenizes the input text into a list of Token objects.
        Args:
            text (str): The input text to be tokenized.
            Returns:
            List[Token]: A list of Token objects, each containing the token text, start and end positions.
        """
        encoding = self.tokenizer(
            text,
            return_offsets_mapping=True,
            add_special_tokens=False,
            return_tensors=None,
        )
        tokens = self.tokenizer.tokenize(text)

        return [
            Token(
                id=idx,
                text=tok,
                start=start + 1 if tok.startswith("Ġ") else start,
                end=end,
            )
            for tok, idx, (start, end) in zip(
                tokens, encoding["input_ids"], encoding["offset_mapping"]
            )
        ]
