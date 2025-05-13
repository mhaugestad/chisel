from chisel.pipeline import PreprocessingPipeline
from chisel.loaders.json_html_loader import JSONHTMLLoader
from chisel.parsers.html_tag_parser import HTMLTagParser
from chisel.tokenizers.simple_tokenizer import SimpleWhitespaceTokenizer
from chisel.chunkers.noop_chunker import NoOpChunker
from chisel.labelers.simple_bio_labeler import SimpleBIOLabeler
from chisel.validators.bio_validator import BIOValidator
from chisel.exporters.json_exporter import JSONExporter

pipeline = PreprocessingPipeline(
    loader=JSONHTMLLoader(),
    parser=HTMLTagParser(),
    tokenizer=SimpleWhitespaceTokenizer(),
    chunker=NoOpChunker(),
    labeler=SimpleBIOLabeler(),
    validator=BIOValidator(),
    exporter=JSONExporter()
)

pipeline.run("examples/data/input_sample.json", "examples/data/output_sample.json")
