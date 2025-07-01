# 👗 Example: Processing Fashion Brand NER (JSON Format) with Chisel

This example shows how to preprocess the explosion/ner-fashion-brands dataset into ChiselRecord objects for training transformer-based NER models using BILO labeling.

## 📥 Step 1: Load the Dataset

```
from datasets import load_dataset

ds = load_dataset("explosion/ner-fashion-brands")
```

## 🧩 Step 2: Implement a JSON Span Parser
The dataset provides character-level spans in a spans field. We write a parser that extracts these into Chisel's EntitySpan format.

```
from typing import Tuple, List
from chisel.extraction.base.protocols import Parser
from chisel.extraction.models.models import EntitySpan

class JSONSpanParser(Parser):
    def parse(self, doc: dict) -> Tuple[str, List[EntitySpan]]:
        text = doc["text"]
        entities = [
            EntitySpan(
                text=text[e["start"]:e["end"]],
                start=e["start"],
                end=e["end"],
                label=e["label"]
            )
            for e in doc.get("spans", [])
        ]
        return text, entities
```

## 🔧 Step 3: Initialize Chisel Components

```
from chisel.extraction.tokenizers.hf_tokenizer import HFTokenizer
from chisel.extraction.span_aligners.token_span_aligner import TokenSpanAligner
from chisel.extraction.labelers.bilo_labeler import BILOLabeler
from chisel.extraction.labelers.label_encoder import SimpleLabelEncoder
from chisel.extraction.validators.validators import DefaultParseValidator, HFTokenAlignmentValidator
from chisel.extraction.formatters.torch_formatter import TorchDatasetFormatter
from chisel.extraction.models.models import ChiselRecord
```

## Component Setup
```
parser = JSONSpanParser()
tokenizer = HFTokenizer(model_name="bert-base-cased")
aligner = TokenSpanAligner()
labeler = BILOLabeler()

label_encoder = SimpleLabelEncoder(label_to_id={
    'O': 0,
    'B-FASHION_BRAND': 1,
    'I-FASHION_BRAND': 2,
    'L-FASHION_BRAND': 3,
    'U-FASHION_BRAND': 4,
})

parse_validators = [DefaultParseValidator(on_error="raise")]
label_validators = [HFTokenAlignmentValidator(tokenizer=tokenizer.tokenizer, on_error="raise")]
formatter = TorchDatasetFormatter()
```

## 🔄 Step 4: Run the Preprocessing Pipeline
```
processed_data = []

for idx, example in enumerate(ds["train"]):
    text, entities = parser.parse(example)

    # 🧪 Per-span validation — skip bad spans
    valid_spans = []
    for span in entities:
        try:
            for validator in parse_validators:
                validator.validate(text, span)
            valid_spans.append(span)
        except ValueError:
            continue 

    tokens = tokenizer.tokenize(text)
    token_entity_spans = aligner.align(entities, tokens)

    labels = labeler.label(tokens, token_entity_spans)
    encoded_labels = label_encoder.encode(labels)

    # 🧪 Per-span validation — skip bad spans
    valid_token_spans = []
    for span in token_entity_spans:
        try:
            for validator in label_validators:
                validator.validate(tokens, span)
            valid_token_spans.append(span)
        except ValueError:
            continue  # Optionally log or collect stats on dropped spans

    record = ChiselRecord(
        id=str(idx),
        chunk_id=0,
        text=tokenizer.tokenizer.decode([token.id for token in tokens]),
        tokens=tokens,
        input_ids=[token.id for token in tokens],
        attention_mask=[1] * len(tokens),
        entities=[tes.entity for tes in valid_token_spans],
        bio_labels=labels,
        labels=encoded_labels
    )
    processed_data.append(record)

data = formatter.format(processed_data)
```

### ✅ Output
You now have a torch dataset ready for training!