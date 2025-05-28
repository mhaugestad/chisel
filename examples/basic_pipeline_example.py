from chisel.pipeline import PreprocessingPipeline
from chisel.loaders.json_html_loader import JSONHTMLLoader
from chisel.parsers.html_tag_parser import HTMLTagParser
from chisel.tokenizers.simple_tokenizer import SimpleWhitespaceTokenizer
from chisel.tokenizers.hf_tokenizer import HFTokenizer
from chisel.chunkers.noop_chunker import NoOpChunker
from chisel.labelers.bio_labeler import BIOLabeler
from chisel.validators.bio_validator import BIOValidator
from chisel.exporters.json_exporter import JSONExporter

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
