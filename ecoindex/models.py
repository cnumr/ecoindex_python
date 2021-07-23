from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel


class Ecoindex(BaseModel):
    grade: Optional[Literal["A", "B", "C", "D", "E", "F", "G"]] = None
    score: Optional[float] = None
    ges: Optional[float] = None
    water: Optional[float] = None
