from datasets import Dataset
from typing import List, Dict
from chisel.base.protocols import Exporter
import os

class HuggingFaceExporter:
    def __init__(
        self,
        output_dir: str,
        dataset_name: str = "chisel_dataset",
        push_to_hub: bool = False,
        hub_repo_id: str | None = None,
        private: bool = True
    ):
        self.output_dir = output_dir
        self.dataset_name = dataset_name
        self.push_to_hub = push_to_hub
        self.hub_repo_id = hub_repo_id
        self.private = private

        if self.push_to_hub and not self.hub_repo_id:
            raise ValueError("hub_repo_id must be provided when push_to_hub=True")

    def export(self, data: List[Dict]) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

        dataset = Dataset.from_list(data)
        dataset.save_to_disk(os.path.join(self.output_dir, self.dataset_name))

        if self.push_to_hub:
            dataset.push_to_hub(repo_id=self.hub_repo_id, private=self.private)


# ✅ Example Usage

# exporter = HuggingFaceExporter(output_dir="datasets/")
# exporter.export([
#     {"id": "1", "tokens": ["Obama"], "labels": ["B-PER"]},
#     {"id": "2", "tokens": ["UNICEF"], "labels": ["B-ORG"]}
# ])


# from datasets import load_from_disk
# ds = load_from_disk("datasets/chisel_dataset")
# print(ds[0])



# exporter = HuggingFaceExporter(
#     output_dir="datasets",
#     dataset_name="chisel-dataset",
#     push_to_hub=True,
#     hub_repo_id="your-username/chisel-dataset",
#     private=True
# )

# exporter.export([
#     {"id": "1", "tokens": ["Obama"], "labels": ["B-PER"]},
#     {"id": "2", "tokens": ["UNICEF"], "labels": ["B-ORG"]}
# ])