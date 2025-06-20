import pytest
from chisel.extraction.labelers.label_encoder import SimpleLabelEncoder


def test_encode_decode_basic():
    encoder = SimpleLabelEncoder(label_to_id={"O": 0, "B-PER": 1, "I-PER": 2})
    labels = ["O", "B-PER", "I-PER"]
    encoded = encoder.encode(labels)
    assert encoded == [0, 1, 2]
    decoded = encoder.decode(encoded)
    assert decoded == labels


def test_encode_unknown_label_strict():
    encoder = SimpleLabelEncoder(label_to_id={"O": 0}, strict=True)
    with pytest.raises(ValueError, match="Unknown label"):
        encoder.encode(["B-PER"])


def test_encode_unknown_label_non_strict_warns():
    encoder = SimpleLabelEncoder(label_to_id={"O": 0}, strict=False)
    with pytest.warns(UserWarning, match="Unknown label 'B-PER'"):
        encoded = encoder.encode(["O", "B-PER"])
    assert encoded == [0, 0]


def test_decode_unknown_id():
    encoder = SimpleLabelEncoder(label_to_id={"O": 0})
    with pytest.raises(ValueError, match="Unknown ID '2'"):
        encoder.decode([0, 2])


def test_label_normalization_success():
    encoder = SimpleLabelEncoder(
        label_to_id={"O": 0, "PER": 1},
        label_normalizer={"PERSON": "PER"},
    )
    encoded = encoder.encode(["O", "PERSON"])
    assert encoded == [0, 1]


def test_label_normalization_invalid_target_raises():
    with pytest.raises(ValueError, match="is not in label_to_id"):
        SimpleLabelEncoder(
            label_to_id={"O": 0},
            label_normalizer={"PERSON": "PER"},
        )


def test_non_strict_requires_O():
    with pytest.raises(ValueError, match="Label 'O' must be in label_to_id"):
        SimpleLabelEncoder(label_to_id={}, strict=False)


def test_get_label_to_id_and_id_to_label():
    mapping = {"O": 0, "B-PER": 1}
    encoder = SimpleLabelEncoder(label_to_id=mapping)
    assert encoder.get_label_to_id() == mapping
    assert encoder.get_id_to_label() == {0: "O", 1: "B-PER"}
