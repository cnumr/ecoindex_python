from typing import Optional

from pkg_resources import get_distribution
from sqlmodel import Field, SQLModel

PageType = str


class Ecoindex(SQLModel):
    grade: Optional[str] = Field(
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
    ecoindex_version: Optional[str] = Field(
        default=get_distribution("ecoindex").version,
        title="Ecoindex version",
        description="Is the version of the ecoindex used to compute the score",
    )
