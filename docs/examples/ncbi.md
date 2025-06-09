# 🧪 Example: Processing the NCBI Disease Dataset with Chisel
This example demonstrates how to preprocess the [NCBI Disease Corpus](https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/) using the Chisel library, transforming the data into a format suitable for transformer-based token classification models.

## 📥 Step 1: Download the NCBI Dataset

The NCBI corpus uses inline HTML-like tags to annotate disease mentions. Annotations look like:

```
<category="SpecificDisease">Cancer</category>
```

To work with this format, we ensure it is valid XML by renaming attributes to:

```
<category category="SpecificDisease">Cancer</category>
```

## ✅ Download and extract the dataset
```
import requests, zipfile, io, os

url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBI_corpus.zip"
extract_to = "./data"
os.makedirs(extract_to, exist_ok=True)

response = requests.get(url)
if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted contents to: {extract_to}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
```

## 📄 Step 2: Load and Clean the Data
```
annotations = []
with open("./data/NCBI_corpus_training.txt", "r") as f:
    for line in f:
        splits = line.split("\t")
        annotations.append({
            "id": splits[0].strip(),
            "text": " ".join(splits[1:]).strip().replace('<category="', '<category category="')
        })
```

## 🧱 Step 3: Preprocess with Chisel
We define and connect the pipeline components from Chisel.


### 🔧 Setup

```
from transformers import AutoTokenizer
from chisel.extraction.parsers.html_tag_parser import HTMLTagParser
from chisel.extraction.tokenizers.hf_tokenizer import HFTokenizer
from chisel.extraction.chunkers.fixed_length_chunker import FixedLengthTokenChunker
from chisel.extraction.span_aligners.token_span_aligner import TokenSpanAligner
from chisel.extraction.labelers.bio_labeler import BIOLabeler
from chisel.extraction.labelers.label_encoder import SimpleLabelEncoder
from chisel.extraction.validators.validators import DefaultParseValidator, HFTokenAlignmentValidator
from chisel.extraction.models.models import ChiselRecord
```


### 🧩 Components

```
parser = HTMLTagParser(label_strategy="attribute", attribute_name="category")
tokenizer = HFTokenizer(model_name="bert-base-cased")
aligner = TokenSpanAligner()
chunker = FixedLengthTokenChunker(max_tokens=512, overlap=0)
labeler = BIOLabeler()
label_encoder = SimpleLabelEncoder(label_to_id={
    'O': 0,
    'B-Modifier': 1,
    'I-Modifier': 2,
    'B-SpecificDisease': 3,
    'I-SpecificDisease': 4,
    'B-CompositeMention': 5,
    'I-CompositeMention': 6,
    'B-DiseaseClass': 7,
    'I-DiseaseClass': 8,
})
parse_validators = [DefaultParseValidator()]
label_validators = [HFTokenAlignmentValidator(tokenizer=tokenizer.tokenizer)]
```

### 🔄 Step 4: Run the Pipeline
```
processed_data = []

for example in annotations:
    text, entities = parser.parse(example["text"])

    for validator in parse_validators:
        validator.validate(text, entities)

    tokens = tokenizer.tokenize(text)
    token_entity_spans = aligner.align(entities, tokens)

    token_chunks, entity_chunks = chunker.chunk(tokens, token_entity_spans)

    for chunk_id, (toks, ents) in enumerate(zip(token_chunks, entity_chunks)):
        labels = labeler.label(toks, ents)
        encoded_labels = label_encoder.encode(labels)

        for validator in label_validators:
            validator.validate(toks, ents, labels)

        record = ChiselRecord(
            id=example["id"],
            chunk_id=chunk_id,
            text=tokenizer.tokenizer.decode([token.id for token in toks]),
            tokens=toks,
            input_ids=[token.id for token in toks],
            attention_mask=[1] * len(toks),
            entities=[tes.entity for tes in ents],
            bio_labels=labels,
            labels=encoded_labels
        )
        processed_data.append(record)
```

### ✅ Output
You now have a list of ChiselRecord objects in processed_data, ready for training or export!

