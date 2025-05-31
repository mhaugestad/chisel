from chisel.extraction.tokenizers.hf_tokenizer import HFTokenizer


def test_hf_tokenizer_outputs_tokens_with_offsets():
    tokenizer = HFTokenizer()
    text = "Barack Obama"
    tokens = tokenizer.tokenize(text)

    assert all(t.start < t.end for t in tokens)
    assert "Barack" in [t.text for t in tokens]
