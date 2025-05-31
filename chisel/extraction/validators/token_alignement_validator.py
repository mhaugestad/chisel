from transformers import PreTrainedTokenizerBase
from chisel.extraction.models.models import Token, EntitySpan
from chisel.extraction.base.protocols import Validator
import logging

logger = logging.getLogger(__name__)


class TokenAlignmentValidator(Validator):
    def __init__(self, tokenizer: PreTrainedTokenizerBase):
        self.tokenizer = tokenizer

    def validate(
        self,
        text: str,
        tokens: list[Token],
        entities: list[EntitySpan],
        labels: list[str],
    ) -> None:
        i = 0
        while i < len(labels):
            if labels[i].startswith("B-"):
                entity_tokens = [tokens[i]]
                label = labels[i][2:]
                i += 1
                while i < len(labels) and labels[i].startswith("I-"):
                    entity_tokens.append(tokens[i])
                    i += 1

                entity_text = "".join(token.text for token in entity_tokens).replace(
                    " ", ""
                )
                match = None
                for entity in entities:
                    span_text = entity.text.replace(" ", "")
                    if span_text == entity_text and entity.label == label:
                        match = entity
                        break

                if match is None:
                    raise ValueError(
                        f"Mismatch between token span and entity span for label {label}:\n"
                        f"  Token text: '{entity_text}'\n"
                        f"  Entity options: {[e.text for e in entities if e.label == label]}"
                    )
            else:
                i += 1
