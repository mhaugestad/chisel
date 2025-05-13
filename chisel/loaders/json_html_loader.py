import json
from typing import List, Dict
from chisel.base.protocols import Loader

class JSONHTMLLoader(Loader):
    def load(self, path: str) -> List[Dict]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)