import json
from typing import List, Dict
from chisel.base.protocols import Exporter

class JSONExporter:
    def export(self, data: List[Dict], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)