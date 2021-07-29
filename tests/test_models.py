from ecoindex.models import Ecoindex, Page, Result
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
        "(type=value_error.const; given=dummy; permitted=('A', 'B', 'C', 'D', 'E', 'F', 'G'))"
        in str(error.value)
    )

    assert "value is not a valid float (type=type_error.float)" in str(error.value)


def test_ecoindex_model_empty():
    ecoindex = Ecoindex()
    assert ecoindex.ges == None
    assert ecoindex.grade == None
    assert ecoindex.score == None
    assert ecoindex.water == None


def test_model_page():
    logs = ["Logs of my page"]
    outer_html = "Html of my page"
    nodes = ["node1", "node2", "node3"]

    page = Page(
        logs=logs,
        outer_html=outer_html,
        nodes=nodes,
    )

    assert page.logs == logs
    assert page.outer_html == outer_html
    assert page.nodes == nodes

    with raises(ValidationError):
        Page(logs=logs)


def test_result_model():
    result = Result(size=2500, nodes=500, requests=100)
    assert result.score is None
    assert result.page_type is None
    assert result.size == 2500
    assert result.nodes == 500
    assert result.requests == 100
