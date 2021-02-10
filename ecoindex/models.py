from dataclasses import dataclass
from typing import Optional


@dataclass
class Ecoindex:
    grade: Optional[str] = None
    score: Optional[float] = None
    ges: Optional[float] = None
    water: Optional[float] = None
