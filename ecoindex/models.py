from dataclasses import dataclass


@dataclass
class Ecoindex:
    grade: str
    score: float
    ges: float
    water: float
