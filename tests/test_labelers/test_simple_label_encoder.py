from chisel.extraction.labelers.simple_label_encoder import SimpleLabelEncoder


def test_simple_label_encoder():
    labels_1 = ["B-PER", "I-PER", "O", "B-ORG"]
    labels_2 = ["O", "B-LOC", "I-LOC", "O"]

    encoder = SimpleLabelEncoder()
    encoder.fit([labels_1, labels_2])

    all_labels = labels_1 + labels_2
    encoded = encoder.encode(all_labels)
    decoded = encoder.decode(encoded)

    assert decoded == all_labels
    assert encoder.label2id("B-PER") == encoder.label_to_id["B-PER"]
    assert encoder.id2label(encoder.label_to_id["O"]) == "O"
