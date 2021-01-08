from typing import List, Union

from ecoindex.models import Ecoindex
from ecoindex.quantiles import quantiles_dom, quantiles_req, quantiles_size


def get_quantile(quantiles: List[Union[int, float]], value: Union[int, float]) -> float:
    for i in range(1, len(quantiles) + 1):
        if value < quantiles[i]:
            return i + (value - quantiles[i - 1]) / (quantiles[i] - quantiles[i - 1])

    return len(quantiles)


def get_score(dom: int, size: float, requests: int) -> float:
    q_dom = get_quantile(quantiles_dom, dom)
    q_size = get_quantile(quantiles_size, size)
    q_req = get_quantile(quantiles_req, requests)

    return round(100 - 5 * (3 * q_dom + 2 * q_req + q_size) / 6)


def get_ecoindex(dom: int, size: float, requests: int) -> Ecoindex:
    score = get_score(dom=dom, size=size, requests=requests)

    return Ecoindex(
        score=score,
        grade=get_grade(score),
        ges=get_greenhouse_gases_emmission(score),
        water=get_water_consumption(score),
    )


def get_grade(ecoindex: float) -> str:
    if ecoindex > 75:
        return "A"
    if ecoindex > 65:
        return "B"
    if ecoindex > 50:
        return "C"
    if ecoindex > 35:
        return "D"
    if ecoindex > 20:
        return "E"
    if ecoindex > 5:
        return "F"
    return "G"


def get_greenhouse_gases_emmission(ecoindex: float) -> float:
    return round(100 * (2 + 2 * (50 - ecoindex) / 100)) / 100


def get_water_consumption(ecoindex: float) -> float:
    return round(100 * (3 + 3 * (50 - ecoindex) / 100)) / 100
