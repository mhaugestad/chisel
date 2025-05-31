import json
from typing import List, Dict


class JSONExporter:

    def __init__(self, output_path: str):
        """
        Initializes the JSONExporter with a specified output path.
        Args:
            output_path (str): Path where the JSON file will be saved.
        """
        self.output_path = output_path

    def export(self, data: List[Dict]) -> None:
        """
        Exports the provided data to a JSON file.
        Args:
            data (List[Dict]): List of dictionaries containing the dataset entries.
        """
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
