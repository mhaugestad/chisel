from chisel.tokenizers.spacy_tokenizer import SpacyTokenizer

def test_spacy_tokenizer_outputs_tokens_with_offsets():
    tokenizer = SpacyTokenizer()
    text = "Barack Obama"
    tokens = tokenizer.tokenize(text)

    assert tokens[0].text == "Barack"
    assert tokens[1].text == "Obama"
    assert tokens[0].start == text.index("Barack")
