import json
from typing import List, Dict
from chisel.base.protocols import Exporter

class JSONExporter:

    def __init__(self, output_path: str):
        self.output_path = output_path

    def export(self, data: List[Dict]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)