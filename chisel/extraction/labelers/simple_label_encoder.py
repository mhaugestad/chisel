from typing import List, Dict


class SimpleLabelEncoder:
    def __init__(self) -> None:
        self.label_to_id: Dict[str, int] = {}
        self.id_to_label: Dict[int, str] = {}

    def fit(self, label_lists: List[List[str]]) -> None:
        """Build label vocabulary from list of label sequences."""
        unique_labels = sorted(set(label for seq in label_lists for label in seq))
        self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}

    def encode(self, labels: List[str]) -> List[int]:
        return [self.label_to_id[label] for label in labels]

    def decode(self, ids: List[int]) -> List[str]:
        return [self.id_to_label[idx] for idx in ids]

    def label2id(self, label: str) -> int:
        return self.label_to_id[label]

    def id2label(self, idx: int) -> str:
        return self.id_to_label[idx]
