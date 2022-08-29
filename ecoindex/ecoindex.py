from typing import List, Union

from ecoindex.models import Ecoindex
from ecoindex.quantiles import quantiles_dom, quantiles_req, quantiles_size


async def get_quantile(
    quantiles: List[Union[int, float]], value: Union[int, float]
) -> float:
    for i in range(1, len(quantiles) + 1):
        if value < quantiles[i]:
            return (
                i - 1 + (value - quantiles[i - 1]) / (quantiles[i] - quantiles[i - 1])
            )

    return len(quantiles) - 1


async def get_score(dom: int, size: float, requests: int) -> float:
    q_dom = await get_quantile(quantiles_dom, dom)
    q_size = await get_quantile(quantiles_size, size)
    q_req = await get_quantile(quantiles_req, requests)

    return round(100 - 5 * (3 * q_dom + 2 * q_req + q_size) / 6)


async def get_ecoindex(dom: int, size: float, requests: int) -> Ecoindex:
    score = await get_score(dom=dom, size=size, requests=requests)

    return Ecoindex(
        score=score,
        grade=await get_grade(score),
        ges=await get_greenhouse_gases_emmission(score),
        water=await get_water_consumption(score),
    )


async def get_grade(ecoindex: float) -> str:
    if ecoindex > 80:
        return "A"
    if ecoindex > 70:
        return "B"
    if ecoindex > 55:
        return "C"
    if ecoindex > 40:
        return "D"
    if ecoindex > 25:
        return "E"
    if ecoindex > 10:
        return "F"
    return "G"


async def get_greenhouse_gases_emmission(ecoindex: float) -> float:
    return round(100 * (2 + 2 * (50 - ecoindex) / 100)) / 100


async def get_water_consumption(ecoindex: float) -> float:
    return round(100 * (3 + 3 * (50 - ecoindex) / 100)) / 100
