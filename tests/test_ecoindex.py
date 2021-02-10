from ecoindex.ecoindex import (
    get_ecoindex,
    get_grade,
    get_greenhouse_gases_emmission,
    get_quantile,
    get_score,
    get_water_consumption,
)
from ecoindex.models import Ecoindex
from ecoindex.quantiles import quantiles_dom, quantiles_req, quantiles_size


def test_ecoindex_model_empty():
    ecoindex = Ecoindex()
    assert ecoindex.ges == None
    assert ecoindex.grade == None
    assert ecoindex.score == None
    assert ecoindex.water == None


def test_ecoindex_model():
    ecoindex = Ecoindex(grade="C", score=34.5, ges=12.1, water=5.3)
    assert ecoindex.ges == 12.1
    assert ecoindex.grade == "C"
    assert ecoindex.score == 34.5
    assert ecoindex.water == 5.3


def test_get_quantiles():
    quantile_size = get_quantile(quantiles_size, 2500)
    assert quantile_size == 15.086372025739513

    quantile_dom = get_quantile(quantiles_dom, 150)
    assert quantile_dom == 3.892857142857143

    quantile_req = get_quantile(quantiles_req, 23)
    assert quantile_req == 3.8


def test_get_score():
    assert get_score(dom=100, requests=100, size=100) == 67
    assert get_score(dom=100, requests=100, size=1000) == 62
    assert get_score(dom=100, requests=100, size=10000) == 53
    assert get_score(dom=200, requests=200, size=10000) == 41
    assert get_score(dom=2355, requests=267, size=2493) == 5
    assert get_score(dom=240, requests=20, size=331) == 78


def test_get_grade():
    assert get_grade(2) == "G"
    assert get_grade(10) == "F"
    assert get_grade(25) == "E"
    assert get_grade(10) == "F"
    assert get_grade(50.2) == "C"
    assert get_grade(10) == "F"
    assert get_grade(100) == "A"


def test_get_ecoindex():
    assert get_ecoindex(dom=100, requests=100, size=100) == Ecoindex(
        score=67,
        grade="B",
        ges=1.66,
        water=2.49,
    )


def test_get_greenhouse_gases_emission():
    assert get_greenhouse_gases_emmission(2) == 2.96
    assert get_greenhouse_gases_emmission(10) == 2.8
    assert get_greenhouse_gases_emmission(50) == 2
    assert get_greenhouse_gases_emmission(70) == 1.6


def test_get_water_consumption():
    assert get_water_consumption(2) == 4.44
    assert get_water_consumption(10) == 4.2
    assert get_water_consumption(50) == 3
    assert get_water_consumption(70) == 2.4
