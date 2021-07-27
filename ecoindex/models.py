from pprint import pprint
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Ecoindex(BaseModel):
    grade: Optional[Literal["A", "B", "C", "D", "E", "F", "G"]] = Field(
        default=None,
        title="Ecoindex grade",
        description="Is the corresponding ecoindex grade of the page (from A to G)",
    )
    score: Optional[float] = Field(
        default=None,
        title="Ecoindex score",
        description="Is the corresponding ecoindex score of the page (0 to 100)",
        ge=0,
        le=100,
    )
    ges: Optional[float] = Field(
        default=None,
        title="Ecoindex GES equivalent",
        description="Is the equivalent of greenhouse gases emission (in `gCO2e`) of the page",
        ge=0,
    )
    water: Optional[float] = Field(
        default=None,
        title="Ecoindex Water equivalent",
        description="Is the equivalent water consumption (in `cl`) of the page",
        ge=0,
    )


pprint(Ecoindex.schema_json())
