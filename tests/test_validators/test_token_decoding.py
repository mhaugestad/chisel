import pytest
from typing import List
from transformers import AutoTokenizer
from transformers import PreTrainedTokenizerBase
from chisel.extraction.models.models import Token

# 👇 This is the function we will eventually implement/fix
def decode_token_span(tokenizer: PreTrainedTokenizerBase, tokens: List[Token]) -> str:
    """
    Decodes a span of Token objects into plain text, accounting for tokenizer-specific subword prefixes.

    Parameters
    ----------
    tokenizer : PreTrainedTokenizerBase
        The Hugging Face tokenizer used for encoding.
    tokens : List[Token]
        The list of token objects (with .id and .text).

    Returns
    -------
    str
        The decoded natural text corresponding to the token span.
    """
    token_ids = [token.id for token in tokens]

    # Try using the tokenizer's native decoding
    try:
        decoded = tokenizer.decode(token_ids, skip_special_tokens=True).strip()
    except Exception:
        decoded = None

    # If decoding fails or produces known inconsistencies, fall back to string-join
    if not decoded or decoded.count("�") > 0:
        # Fallback 1: use tokenizer.convert_tokens_to_string
        try:
            token_texts = [tokenizer.convert_ids_to_tokens(tid) for tid in token_ids]
            decoded = tokenizer.convert_tokens_to_string(token_texts).strip()
        except Exception:
            # Fallback 2: crude reconstruction
            decoded = " ".join(t.text for t in tokens)

    return decoded


@pytest.fixture
def tokenizer():
    return AutoTokenizer.from_pretrained("bert-base-cased")

def test_decode_simple_tokens(tokenizer):
    tokens = tokenizer.tokenize("dog barked")
    ids = tokenizer.convert_tokens_to_ids(tokens)

    token_objs = [
        Token(id=ids[0], text="dog", start=0, end=3),
        Token(id=ids[1], text="barked", start=4, end=10)
    ]
    decoded = decode_token_span(tokenizer, token_objs)
    assert decoded == "dog barked"

def test_decode_with_subword_tokens(tokenizer):
    text = "he said"
    tokens = tokenizer.tokenize(text)
    ids = tokenizer.convert_tokens_to_ids(tokens)

    assert tokens == ["he", "said"]

    token_objs = [
        Token(id=ids[0], text="he", start=0, end=2),
        Token(id=ids[1], text="##said", start=3, end=7),  # emulate stripped text
    ]

    decoded = decode_token_span(tokenizer, token_objs)
    # ❌ This will currently fail with "he ##said" or "he said" depending on tokenizer.decode
    assert decoded == "he said"

def test_decode_isolated_subword_token_fails(tokenizer):
    text = "said"
    tokens = tokenizer.tokenize(text)
    ids = tokenizer.convert_tokens_to_ids(tokens)

    # This may return "##said" or " said"
    token_objs = [Token(id=ids[0], text="said", start=0, end=4)]
    decoded = decode_token_span(tokenizer, token_objs)

    # This assertion is expected to fail until we fix the tokenizer strategy
    assert decoded == "said"


@pytest.mark.parametrize("model_name,tokens_expected,text", [
    ("bert-base-cased", ["he", "##said"], "he said"),               # WordPiece
    ("roberta-base", ["Ġhe", "Ġsaid"], "he said"),                  # BPE (GPT-2 style, with space encoded)
    ("gpt2", ["he", "Ġsaid"], "he said"),                           # GPT-2 BPE (space in prefix)
    ("xlm-roberta-base", ["▁he", "▁said"], "he said"),              # SentencePiece
])
def test_subword_decoding_variants(model_name, tokens_expected, text):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)

    assert tokens == tokens_expected or tokenizer.convert_tokens_to_string(tokens) == text, \
        f"Unexpected tokens: {tokens} for model {model_name}"

    ids = tokenizer.convert_tokens_to_ids(tokens)

    token_objs = []
    offset = 0
    for token, id_ in zip(tokens, ids):
        token_stripped = token.replace("Ġ", "").replace("▁", "").replace("##", "")
        token_objs.append(Token(id=id_, text=token_stripped, start=offset, end=offset + len(token_stripped)))
        offset += len(token_stripped) + 1  # assume space between tokens

    decoded = decode_token_span(tokenizer, token_objs)

    # 🧪 Assertion — expect full clean decoding
    assert decoded == text, f"Decoded '{decoded}' != expected '{text}' for model {model_name}'"
