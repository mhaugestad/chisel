from typing import List
from chisel.models.models import Token, EntitySpan


class BIOAlignmentValidator:
    def __init__(self, ignore_whitespace: bool = True):
        self.ignore_whitespace = ignore_whitespace

    def validate(self, tokens: List[Token], labels: List[str], entities: List[EntitySpan]) -> List[str]:
        """
        Validates that BIO-labeled spans correctly reconstruct the EntitySpan text.
        Returns a list of error messages if mismatches are found.
        """
        errors = []
        current_entity = []
        current_label = None
        current_start = None

        for i, label in enumerate(labels):
            if label.startswith("B-"):
                if current_entity:
                    errors.append(f"Unclosed entity before index {i}: {current_label}")
                    current_entity = []

                current_label = label[2:]
                current_entity = [tokens[i].text]
                current_start = tokens[i].start

            elif label.startswith("I-") and current_entity:
                current_entity.append(tokens[i].text)

            elif label.startswith("I-") and not current_entity:
                errors.append(f"Unexpected I- tag without preceding B- at index {i}")

            else:  # label is "O" or some invalid format
                if current_entity:
                    stitched = "".join(current_entity)
                    span = self._find_span(current_start, tokens[i - 1].end, current_label, entities)

                    if span:
                        gold_text = span.text
                        if self.ignore_whitespace:
                            stitched = stitched.replace(" ", "")
                            gold_text = gold_text.replace(" ", "")

                        if stitched != gold_text:
                            errors.append(
                                f"Mismatch for entity '{current_label}' at {span.start}-{span.end}: "
                                f"expected '{span.text}', got '{''.join(current_entity)}'"
                            )
                    else:
                        errors.append(f"No matching span found for entity '{current_label}' starting at {current_start}")

                    current_entity = []
                    current_label = None
                    current_start = None

        return errors

    def _find_span(self, start: int, end: int, label: str, spans: List[EntitySpan]) -> EntitySpan | None:
        for span in spans:
            if span.start == start and span.end == end and span.label == label:
                return span
        return None
