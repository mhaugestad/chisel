import warnings
from typing import Dict, List, Optional


class SimpleLabelEncoder:
    """
    A simple label encoder for converting label strings to integer IDs and back.

    This class is designed for sequence labeling tasks such as Named Entity Recognition (NER).
    It supports optional normalization of label names and graceful handling of unknown labels.

    Parameters
    ----------
    label_to_id : Dict[str, int]
        A dictionary mapping label strings to integer IDs.
        Must include at least the 'O' label if strict=False.

    label_normalizer : Optional[Dict[str, str]], default=None
        A dictionary for normalizing label names before encoding.
        For example, {"PERSON": "PER"} will convert 'PERSON' to 'PER' before lookup.
        Normalized values must exist in `label_to_id`.

    strict : bool, default=True
        If True, raises a ValueError on unknown or unnormalized labels.
        If False, unknown labels are substituted with 'O' and a warning is issued.

    Attributes
    ----------
    label_to_id : Dict[str, int]
        The original label-to-ID mapping.

    id_to_label : Dict[int, str]
        The reverse mapping from ID to label.

    label_normalizer : Dict[str, str]
        The mapping used for label normalization.
    """

    def __init__(
        self,
        label_to_id: Dict[str, int],
        label_normalizer: Optional[Dict[str, str]] = None,
        strict: bool = True,
    ):
        self.label_to_id = label_to_id
        self.id_to_label = {v: k for k, v in self.label_to_id.items()}
        self.label_normalizer = label_normalizer or {}
        self.strict = strict

        for original, mapped in self.label_normalizer.items():
            if mapped not in self.label_to_id:
                raise ValueError(
                    f"Normalizer maps '{original}' -> '{mapped}', "
                    f"but '{mapped}' is not in label_to_id."
                )

        if not self.strict and "O" not in self.label_to_id:
            raise ValueError("Label 'O' must be in label_to_id if strict=False.")

    def encode(self, labels: List[str]) -> List[int]:
        encoded = []
        for label in labels:
            normalized = self.label_normalizer.get(label, label)
            if normalized not in self.label_to_id:
                if self.strict:
                    raise ValueError(
                        f"Unknown label '{label}' (normalized as '{normalized}')."
                    )
                warnings.warn(
                    f"Unknown label '{label}' (normalized as '{normalized}'). "
                    f"Substituting with 'O'."
                )
                normalized = "O"
            encoded.append(self.label_to_id[normalized])
        return encoded

    def decode(self, ids: List[int]) -> List[str]:
        decoded = []
        for i in ids:
            if i not in self.id_to_label:
                raise ValueError(f"Unknown ID '{i}' encountered during decoding.")
            decoded.append(self.id_to_label[i])
        return decoded

    def get_label_to_id(self) -> Dict[str, int]:
        return self.label_to_id

    def get_id_to_label(self) -> Dict[int, str]:
        return self.id_to_label
