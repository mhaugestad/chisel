# chisel/parsers/conll_parser.py

from typing import Tuple, List
from chisel.extraction.base.protocols import Parser
from chisel.extraction.models.models import EntitySpan
import string


class ConllParser(Parser):
    def __init__(self, sep: str = " ", joiner: str = " ", scheme: str = "BIO"):
        """
        Initialize the CoNLL parser.
        Parameters:
        ----------
        sep : str
            The separator used in the CoNLL format (default is space).
        joiner : str
            The string used to join tokens in the reconstructed text (default is space).
        scheme : str
            The annotation scheme used (default is "BIO"). It can be "BIO", "IOB", or "IOB2".
        """
        self.sep = sep
        self.joiner = joiner
        self.scheme = scheme.upper()

    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        """
        Parse a CoNLL-style annotated document.

        Parameters:
        ----------
        doc : str
            A newline-separated string of "token label" pairs.

        Returns:
        -------
        Tuple[str, List[EntitySpan]]
            The reconstructed text and entity spans.
        """
        tokens, labels = [], []
        for line in doc.strip().splitlines():
            if not line.strip():
                continue
            token, label = line.strip().split(self.sep)
            tokens.append(token)
            labels.append(label)

        text = ""
        spans = []
        char_offset = 0
        i = 0

        while i < len(tokens):
            token = tokens[i]
            label = labels[i]

            # Only add joiner if previous token exists and current token is not punctuation
            if text and token not in string.punctuation:
                text += self.joiner
                char_offset += len(self.joiner)

            if label.startswith("B-"):
                ent_label = label[2:]
                ent_start = char_offset
                ent_text = token
                text += token
                char_offset += len(token)
                i += 1
                while i < len(tokens) and labels[i].startswith("I-"):
                    text += self.joiner + tokens[i]
                    ent_text += self.joiner + tokens[i]
                    char_offset += len(self.joiner) + len(tokens[i])
                    i += 1
                ent_end = char_offset
                spans.append(
                    EntitySpan(
                        text=ent_text, start=ent_start, end=ent_end, label=ent_label
                    )
                )
            else:
                text += token
                char_offset += len(token)
                i += 1

        return text.strip(), spans
