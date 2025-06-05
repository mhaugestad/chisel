from typing import List
from datasets import Dataset, DatasetDict
from chisel.extraction.models.models import ChiselRecord


class DatasetExporter:
    """
    Exports ChiselRecords to Hugging Face `datasets.Dataset`, keeping only token classification fields:
    - id
    - tokens
    - input_ids
    - attention_mask
    - labels
    """

    def __init__(self, output_path: str, split: str = "train"):
        self.output_path = output_path
        self.split = split

    def export(self, data: List[ChiselRecord]) -> Dataset:
        dict_data = []

        for record in data:
            record_dict = record.dict()
            dict_data.append(
                {
                    "id": record_dict["id"],
                    "tokens": record_dict["tokens"],
                    "input_ids": record_dict["input_ids"],
                    "attention_mask": record_dict["attention_mask"],
                    "labels": record_dict["labels"],
                }
            )

        dataset = Dataset.from_list(dict_data)
        dataset_dict = DatasetDict({self.split: dataset})
        dataset_dict.save_to_disk(self.output_path)
        return dataset
