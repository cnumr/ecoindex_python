import pytest
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


@pytest.mark.asyncio
class TestAsyncGroup:
    async def test_get_quantiles(self):
        quantile_size = await get_quantile(quantiles_size, 2500)
        assert quantile_size == 14.086372025739513

        quantile_dom = await get_quantile(quantiles_dom, 150)
        assert quantile_dom == 2.892857142857143

        quantile_req = await get_quantile(quantiles_req, 23)
        assert quantile_req == 2.8

    async def test_get_score(self):
        assert await get_score(dom=100, requests=100, size=100) == 72
        assert await get_score(dom=100, requests=100, size=1000) == 67
        assert await get_score(dom=100, requests=100, size=10000) == 58
        assert await get_score(dom=200, requests=200, size=10000) == 46
        assert await get_score(dom=2355, requests=267, size=2493) == 10
        assert await get_score(dom=240, requests=20, size=331) == 83

    async def test_get_ecoindex(self):
        assert await get_ecoindex(dom=100, requests=100, size=100) == Ecoindex(
            score=72,
            grade="B",
            ges=1.56,
            water=2.34,
        )

    async def test_get_grade(self):
        assert await get_grade(2) == "G"
        assert await get_grade(25) == "F"
        assert await get_grade(10) == "G"
        assert await get_grade(50.2) == "D"
        assert await get_grade(100) == "A"

    async def test_get_greenhouse_gases_emission(self):
        assert await get_greenhouse_gases_emmission(2) == 2.96
        assert await get_greenhouse_gases_emmission(10) == 2.8
        assert await get_greenhouse_gases_emmission(50) == 2
        assert await get_greenhouse_gases_emmission(70) == 1.6

    async def test_get_water_consumption(self):
        assert await get_water_consumption(2) == 4.44
        assert await get_water_consumption(10) == 4.2
        assert await get_water_consumption(50) == 3
        assert await get_water_consumption(70) == 2.4
