from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


class Ecoindex(BaseModel):
    grade: Literal["A", "B", "C", "D", "E", "F", "G"]
    score: float
    ges: float
    water: float
