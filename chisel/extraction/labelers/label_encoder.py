from typing import List, Dict


class SimpleLabelEncoder:
    """
    A simple label encoder that supports fitting, encoding, and decoding
    label sequences for classification tasks.

    You can either:
    - Call `fit()` with training labels to build the vocabulary, or
    - Provide `labels` explicitly during initialization.
    """

    def __init__(self, label_to_id: Dict[str, int]):
        self.label_to_id = label_to_id
        self.id_to_label = {v: k for k, v in self.label_to_id.items()}

    def encode(self, labels: List[str]) -> List[int]:
        if not self.label_to_id:
            raise ValueError(
                "LabelEncoder has not been fitted or initialized with labels."
            )
        try:
            return [self.label_to_id[label] for label in labels]
        except KeyError as e:
            raise ValueError(
                f"Unknown label '{e.args[0]}' encountered during encoding."
            ) from e

    def decode(self, ids: List[int]) -> List[str]:
        if not self.id_to_label:
            raise ValueError(
                "LabelEncoder has not been fitted or initialized with labels."
            )
        try:
            return [self.id_to_label[i] for i in ids]
        except KeyError as e:
            raise ValueError(
                f"Unknown ID '{e.args[0]}' encountered during decoding."
            ) from e

    def get_label_to_id(self) -> dict:
        return self.label_to_id

    def get_id_to_label(self) -> dict:
        return self.id_to_label
