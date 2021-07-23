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
        Ecoindex(grade="dummy")

    assert (
        "(type=value_error.const; given=dummy; permitted=('A', 'B', 'C', 'D', 'E', 'F', 'G'))"
        in str(error.value)
    )

    assert "4 validation errors for Ecoindex" in str(error.value)

    assert "field required (type=value_error.missing)" in str(error.value)
