import json
from typing import List, Dict
from chisel.extraction.base.protocols import Loader


class JSONHTMLLoader(Loader):
    """Loader for JSON files containing HTML data.
    This loader reads a JSON file and returns its content as a list of dictionaries.
    Each dictionary represents an entry in the JSON file.
    """

    def load(self, path: str) -> List[Dict]:
        """Loads a JSON file from the specified path.
        Args:
            path (str): Path to the JSON file.
        Returns:
            List[Dict]: A list of dictionaries containing the data from the JSON file.
        """
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
