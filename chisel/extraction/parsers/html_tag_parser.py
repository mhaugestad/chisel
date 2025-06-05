from bs4 import BeautifulSoup, Tag
from typing import List, Tuple, Optional, Set, Literal
from chisel.extraction.models.models import EntitySpan
from chisel.extraction.base.protocols import Parser


class HTMLTagParser(Parser):
    def __init__(
        self,
        label_strategy: Literal["tag", "attribute"] = "tag",
        attribute_name: Optional[str] = None,
        excluded_tags: Optional[Set[str]] = None,
        allow_nested: bool = False,
    ):
        """
        Initializes the HTMLTagParser.
        Parameters:
        ----------
        label_strategy : Literal["tag", "attribute"]
            Strategy to determine the label for each entity span. If "tag", uses the tag name.
            If "attribute", uses the specified attribute's value.
        attribute_name : Optional[str]
            The name of the attribute to use for labeling when label_strategy is "attribute".
        excluded_tags : Optional[Set[str]]
            Set of HTML tags to exclude from annotation. Default excludes common structural tags.
        allow_nested : bool
            If True, allows nested tags to be processed and annotated. If False, only the outermost
            tags are annotated.
        """
        self.label_strategy = label_strategy
        self.attribute_name = attribute_name
        self.excluded_tags = excluded_tags or {"html", "body", "div", "p", "span"}
        self.allow_nested = allow_nested

    def _extract_label(self, tag: Tag) -> str:
        if self.label_strategy == "tag":
            return tag.name.upper()
        elif self.label_strategy == "attribute":
            return tag.attrs.get(self.attribute_name, tag.name.upper())
        else:
            raise ValueError(f"Unsupported label strategy: {self.label_strategy}")

    def _is_annotation_tag(self, tag: Tag) -> bool:
        return tag.name not in self.excluded_tags

    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        soup = BeautifulSoup(doc, "html.parser")
        clean_text = ""
        entities: List[EntitySpan] = []

        def handle_node(node) -> str:
            nonlocal clean_text, entities

            if isinstance(node, Tag):
                if self._is_annotation_tag(node):
                    if self.allow_nested:
                        inner_text = ""
                        for child in node.children:
                            inner_text += handle_node(child)
                    else:
                        inner_text = node.get_text()

                    label = self._extract_label(node)
                    attributes = {k: v for k, v in node.attrs.items()}
                    start = len(clean_text)
                    end = start + len(inner_text)
                    entities.append(
                        EntitySpan(
                            text=inner_text,
                            start=start,
                            end=end,
                            label=label,
                            attributes=attributes,
                        )
                    )
                    return inner_text
                else:
                    # Process children but skip annotating this tag
                    inner_text = ""
                    for child in node.children:
                        inner_text += handle_node(child)
                    return inner_text
            elif isinstance(node, str):
                return node
            return ""

        for child in soup.contents:
            clean_text += handle_node(child)
        return clean_text, entities
