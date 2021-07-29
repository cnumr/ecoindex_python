from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from pydantic.networks import HttpUrl

PageType = str


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


class Page(BaseModel):
    logs: List
    outer_html: str
    nodes: List


class PageMetrics(BaseModel):
    size: float
    nodes: int
    requests: int


class WindowSize(BaseModel):
    height: int
    width: int

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class Result(Ecoindex, PageMetrics):
    url: Optional[HttpUrl] = None
    date: Optional[datetime] = None
    resolution: Optional[WindowSize] = None
    page_type: Optional[PageType] = None
