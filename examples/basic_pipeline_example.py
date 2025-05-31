from chisel.extraction.pipeline import PreprocessingPipeline
from chisel.extraction.loaders.json_html_loader import JSONHTMLLoader
from chisel.extraction.parsers.html_tag_parser import HTMLTagParser
from chisel.extraction.tokenizers.simple_tokenizer import SimpleWhitespaceTokenizer
from chisel.extraction.tokenizers.hf_tokenizer import HFTokenizer
from chisel.extraction.chunkers.noop_chunker import NoOpChunker
from chisel.extraction.labelers.bio_labeler import BIOLabeler
from chisel.extraction.validators.bio_validator import BIOValidator
from chisel.extraction.exporters.json_exporter import JSONExporter

pipeline = PreprocessingPipeline(
    loader=JSONHTMLLoader(),
    parser=HTMLTagParser(label_strategy="tag", allow_nested=False),
    tokenizer=SimpleWhitespaceTokenizer(),
    chunker=NoOpChunker(),
    labeler=BIOLabeler(),
    validator=BIOValidator(),
    exporter=JSONExporter(output_path="examples/data/output_sample_2.json")
)

pipeline.run("examples/data/input_sample.json")
