from ecoindex.models import Ecoindex
from pydantic import ValidationError
from pytest import raises


def test_model_valid():
    valid_ecoindex = Ecoindex(grade="A", score=99.9, ges=0.6, water=0.1)
    assert valid_ecoindex.grade == "A"
    assert valid_ecoindex.score == 99.9
    assert valid_ecoindex.ges == 0.6
    assert valid_ecoindex.water == 0.1


def test_model_invalid():
    with raises(ValidationError) as error:
        Ecoindex(grade="dummy", score="dummy")

    assert (
        "1 validation error for Ecoindex\nscore\n  value is not a valid float"
        in str(error.value)
    )

    assert "value is not a valid float (type=type_error.float)" in str(error.value)


def test_ecoindex_model_empty():
    ecoindex = Ecoindex()
    assert ecoindex.ges == None
    assert ecoindex.grade == None
    assert ecoindex.score == None
    assert ecoindex.water == None
