from chisel.extraction.base.protocols import Loader, Parser, Tokenizer, TokenChunker, TextChunker, Labeler, Validator, Exporter
from typing import Union, List, Dict

class PreprocessingPipeline:
    def __init__(
        self,
        loader: Loader,
        parser: Parser,
        tokenizer: Tokenizer,
        chunker: TokenChunker | TextChunker,
        labeler: Labeler,
        validators: List[Validator],
        exporter: Exporter
    ):
        self.loader = loader
        self.parser = parser
        self.tokenizer = tokenizer
        self.chunker = chunker
        self.labeler = labeler
        self.validators = validators
        self.exporter = exporter

    def run(self, input_path: str):
        documents = self.loader.load(input_path)
        
        processed = []
        for doc in documents:
            text, spans = self.parser.parse(doc["html"])
            tokens = self.tokenizer.tokenize(text)
            chunks = self.chunker.chunk(tokens, spans)

            for chunk in chunks:
                token_texts = [t.text for t in chunk["tokens"]]
                labels = self.labeler.label(chunk["tokens"], chunk["entities"])

                for validator in self.validators:
                    validator.validate(token_texts, labels)
              
                processed.append({
                    "id": doc["id"],
                    "chunk_id": chunk["chunk_id"],
                    "tokens": token_texts,
                    "labels": labels,  
                })

        self.exporter.export(processed)
