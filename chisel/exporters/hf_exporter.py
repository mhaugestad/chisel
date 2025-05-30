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
        """
        Initializes the HuggingFaceExporter with parameters for exporting datasets.
        Args:
            output_dir (str): Directory where the dataset will be saved.
            dataset_name (str): Name of the dataset to be created.
            push_to_hub (bool): Whether to push the dataset to Hugging Face Hub.
            hub_repo_id (str | None): Repository ID on Hugging Face Hub if pushing to hub.
            private (bool): Whether the dataset should be private when pushed to the hub.
        """
        self.output_dir = output_dir
        self.dataset_name = dataset_name
        self.push_to_hub = push_to_hub
        self.hub_repo_id = hub_repo_id
        self.private = private

        if self.push_to_hub and not self.hub_repo_id:
            raise ValueError("hub_repo_id must be provided when push_to_hub=True")

    def export(self, data: List[Dict]) -> None:
        """
        Exports the provided data to a Hugging Face dataset format and saves it to disk.
        Args:
            data (List[Dict]): List of dictionaries containing the dataset entries.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        dataset = Dataset.from_list(data)
        dataset.save_to_disk(os.path.join(self.output_dir, self.dataset_name))

        if self.push_to_hub:
            dataset.push_to_hub(repo_id=self.hub_repo_id, private=self.private)