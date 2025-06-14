# 🧪 Example: Processing CoNLL NER Data with Chisel
This example demonstrates how to parse the CoNLL-2003 dataset into Chisel's internal ChiselRecord format, suitable for training transformer-based token classification models.

## 📥 Step 1: Download CoNLL Data
We use the version hosted by the [CrossWeigh](https://github.com/ZihanWangKi/CrossWeigh) repository.

```
import requests

url = "https://raw.githubusercontent.com/ZihanWangKi/CrossWeigh/refs/heads/master/data/conllpp_train.txt"
response = requests.get(url)
docs = response.text.split("-DOCSTART- -X- -X- O\n\n")
docs = list(filter(lambda x: len(x) > 0, docs))
```

## 🧩 Step 2: Define a Parser for CoNLL Format
Note: Whilst this may seem a bit complicated at first glance, with help of generative AI and the validators chisel provide, it should be fairly quick to write own custom parsers.

```
from typing import Tuple, List
from chisel.extraction.base.protocols import Parser
from chisel.extraction.models.models import EntitySpan
import string

class ConllParser(Parser):
    def parse(self, doc: str) -> Tuple[str, List[EntitySpan]]:
        tokens, labels = [], []
        for line in doc.strip().splitlines():
            if not line.strip():
                continue
            splits = line.strip().split(" ")
            tokens.append(splits[0])
            labels.append(splits[-1])

        text = ""
        spans = []
        char_offset = 0
        i = 0

        while i < len(tokens):
            token = tokens[i]
            label = labels[i]

            if text and token not in string.punctuation:
                text += " "
                char_offset += 1

            if label.startswith("B-"):
                ent_label = label[2:]
                ent_start = char_offset
                ent_text = token
                text += token
                char_offset += len(token)
                i += 1
                while i < len(tokens) and labels[i].startswith("I-"):
                    text += " " + tokens[i]
                    ent_text += " " + tokens[i]
                    char_offset += 1 + len(tokens[i])
                    i += 1
                ent_end = char_offset
                spans.append(EntitySpan(text=ent_text, start=ent_start, end=ent_end, label=ent_label))
            else:
                text += token
                char_offset += len(token)
                i += 1

        return text.strip(), spans
```

## 🔧 Step 3: Initialize Chisel Components

```
from transformers import AutoTokenizer
from chisel.extraction.tokenizers.hf_tokenizer import HFTokenizer
from chisel.extraction.span_aligners.token_span_aligner import TokenSpanAligner
from chisel.extraction.labelers.bio_labeler import BIOLabeler
from chisel.extraction.labelers.label_encoder import SimpleLabelEncoder
from chisel.extraction.validators.validators import DefaultParseValidator, HFTokenAlignmentValidator
from chisel.extraction.formatters.hf_formatter import HFDatasetFormatter
from chisel.extraction.models.models import ChiselRecord
```

## 📦 Components

```
parser = ConllParser()
tokenizer = HFTokenizer(model_name="bert-base-cased")
aligner = TokenSpanAligner()
labeler = BIOLabeler()
label_encoder = SimpleLabelEncoder(label_to_id={
    'O': 0,
    'B-ORG': 1,
    'I-ORG': 2,
    'B-PER': 3,
    'I-PER': 4,
    'B-MISC': 5,
    'I-MISC': 6,
    'B-LOC': 7,
    'I-LOC': 8
})

parse_validators = [DefaultParseValidator()]
label_validators = [HFTokenAlignmentValidator(tokenizer=tokenizer.tokenizer)]
formatter = HFDatasetFormatter()
```

## 🔄 Step 4: Run the Pipeline

```
processed_data = []

for idx, example in enumerate(docs):
    text, entities = parser.parse(example)

    for validator in parse_validators:
        validator.validate(text, entities)

    tokens = tokenizer.tokenize(text)
    token_entity_spans = aligner.align(entities, tokens)

    labels = labeler.label(tokens, token_entity_spans)
    encoded_labels = label_encoder.encode(labels)

    for validator in label_validators:
        validator.validate(tokens, token_entity_spans)

    record = ChiselRecord(
        id=str(idx),
        chunk_id=0,
        text=tokenizer.tokenizer.decode([token.id for token in tokens]),
        tokens=tokens,
        input_ids=[token.id for token in tokens],
        attention_mask=[1] * len(tokens),
        entities=[tes.entity for tes in token_entity_spans],
        bio_labels=labels,
        labels=encoded_labels
    )

    processed_data.append(record)

data = formatter.format(processed_data)
```

### ✅ Output
You now have a HuggingFace dataset ready!