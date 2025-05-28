from bs4 import BeautifulSoup
from typing import List, Tuple
from chisel.base.protocols import Parser
from chisel.models.models import EntitySpan

class HTMLTagParser(Parser):

    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        soup = BeautifulSoup(doc, "html.parser")
        clean_text = ""
        entities = []
        offset = 0

        clean_text = ""
        entities = []
        offset = 0

        for el in soup.descendants:
            if el.name:
                entity_text = el.get_text()
                start = len(clean_text)
                clean_text += entity_text
                end = len(clean_text)
                
                entities.append(EntitySpan(
                            text=entity_text,
                            start=start,
                            end=end,
                            label=el.name.upper()
                        ))
                    
            elif isinstance(el, str):
                clean_text += el
        return clean_text, entities