from typing import List
from chisel.extraction.models.models import Token, EntitySpan


class BILOUAlignmentValidator:
    def __init__(self, ignore_whitespace: bool = True):
        self.ignore_whitespace = ignore_whitespace

    def validate(self, tokens: List[Token], labels: List[str], entities: List[EntitySpan]) -> List[str]:
        """
        Validates that BILOU-labeled spans correctly reconstruct the EntitySpan text.
        Returns a list of error messages if mismatches are found.
        """
        errors = []
        i = 0
        while i < len(labels):
            label = labels[i]
            if label.startswith("B-"):
                label_type = label[2:]
                start = tokens[i].start
                pieces = [tokens[i].text]

                i += 1
                while i < len(labels) and labels[i].startswith("I-"):
                    pieces.append(tokens[i].text)
                    i += 1

                if i < len(labels) and labels[i].startswith("L-"):
                    pieces.append(tokens[i].text)
                    end = tokens[i].end
                    i += 1
                else:
                    errors.append(f"Missing L- tag to close entity starting at token {i - len(pieces)}")
                    continue

                stitched = "".join(pieces)
                match = self._find_span(start, end, label_type, entities)
                if not match:
                    errors.append(f"No span found for BIL entity '{label_type}' ({start}-{end})")
                else:
                    if self.ignore_whitespace:
                        stitched = stitched.replace(" ", "")
                        expected = match.text.replace(" ", "")
                    else:
                        expected = match.text
                    if stitched != expected:
                        errors.append(f"Mismatch in BIL entity '{label_type}': got '{stitched}' vs '{match.text}'")

            elif label.startswith("U-"):
                label_type = label[2:]
                start = tokens[i].start
                end = tokens[i].end
                match = self._find_span(start, end, label_type, entities)

                if not match:
                    errors.append(f"No span found for U entity '{label_type}' ({start}-{end})")
                elif (not self.ignore_whitespace and tokens[i].text != match.text) or (
                    self.ignore_whitespace and tokens[i].text.replace(" ", "") != match.text.replace(" ", "")
                ):
                    errors.append(f"Mismatch in U entity '{label_type}': got '{tokens[i].text}' vs '{match.text}'")
                i += 1

            else:
                i += 1

        return errors

    def _find_span(self, start: int, end: int, label: str, spans: List[EntitySpan]) -> EntitySpan | None:
        for span in spans:
            if span.start == start and span.end == end and span.label == label:
                return span
        return None
