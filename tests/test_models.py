from os import rmdir
from os.path import isdir

from pydantic import ValidationError
from pytest import raises

from ecoindex.models import Ecoindex, Result, ScreenShot, WebPage


def test_model_webpage_no_url():
    with raises(ValidationError) as error:
        WebPage()

    assert (
        "1 validation error for WebPage\n"
        "url\n"
        "  field required (type=value_error.missing)"
    ) in str(error.value)


def test_model_webpage_invalid_url():
    with raises(ValidationError) as error:
        WebPage(url="toto")

    assert (
        "1 validation error for WebPage\n"
        "url\n"
        "  invalid or missing URL scheme (type=value_error.url.scheme)"
    ) in str(error.value)


def test_model_webpage_wrong_size():
    with raises(ValidationError) as error:
        WebPage(url="https://www.google.fr", width=0, height=0)

    assert (
        "2 validation errors for WebPage\n"
        "width\n"
        "  ensure this value is greater than or equal to 100 (type=value_error.number.not_ge; limit_value=100)\n"
        "height\n"
        "  ensure this value is greater than or equal to 50 (type=value_error.number.not_ge; limit_value=50)"
    ) in str(error.value)


def test_model_webpage_default_size():
    webpage = WebPage(url="https://www.google.fr")
    assert webpage.height == 1080
    assert webpage.width == 1920


def test_model_valid():
    valid_ecoindex = Ecoindex(grade="A", score=99.9, ges=0.6, water=0.1)
    assert valid_ecoindex.grade == "A"
    assert valid_ecoindex.score == 99.9
    assert valid_ecoindex.ges == 0.6
    assert valid_ecoindex.water == 0.1
    assert valid_ecoindex.ecoindex_version not in [None, ""]


def test_model_invalid():
    with raises(ValidationError) as error:
        Ecoindex(grade="dummy", score="dummy")

    assert (
        "1 validation error for Ecoindex\n" "score\n" "  value is not a valid float"
    ) in str(error.value)

    assert "value is not a valid float (type=type_error.float)" in str(error.value)


def test_ecoindex_model_empty():
    ecoindex = Ecoindex()
    assert ecoindex.ges == None
    assert ecoindex.grade == None
    assert ecoindex.score == None
    assert ecoindex.water == None


def test_result_model():
    result = Result(
        size=119,
        nodes=45,
        requests=8,
        url="http://www.myurl.com",
        width=1920,
        height=1080,
        grade="A",
        score=89,
        ges=1.22,
        water=1.89,
    )
    assert result.page_type is None
    assert result.size == 119
    assert result.nodes == 45
    assert result.requests == 8
    assert result.width == 1920
    assert result.height == 1080
    assert result.grade == "A"
    assert result.score == 89
    assert result.ges == 1.22
    assert result.water == 1.89
    assert result.ecoindex_version is not None


def test_screenshot_model():
    id = "screenshot_test_id"
    folder = "./screenshot_test"

    screenshot = ScreenShot(id=id, folder=folder)

    assert isdir(folder) == True
    assert screenshot.id == id
    assert screenshot.folder == folder
    assert screenshot.get_png() == f"{folder}/{id}.png"
    assert screenshot.get_webp() == f"{folder}/{id}.webp"

    rmdir(folder)
    assert isdir(folder) == False
