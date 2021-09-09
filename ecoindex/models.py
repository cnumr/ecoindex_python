from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.networks import HttpUrl
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


class Page(BaseModel):
    logs: List
    outer_html: str
    nodes: List


class PageMetrics(SQLModel):
    size: float = Field(
        default=...,
        title="Page size",
        description="Is the size of the page and of the downloaded elements of the page in KB",
        ge=0,
    )
    nodes: int = Field(
        default=...,
        title="Page nodes",
        description="Is the number of the DOM elements in the page",
        ge=0,
    )
    requests: int = Field(
        default=...,
        title="Page requests",
        description="Is the number of external requests made by the page",
        ge=0,
    )


class WindowSize(BaseModel):
    height: int = Field(
        default=...,
        title="Window height",
        description="Height of the simulated window in pixel",
    )
    width: int = Field(
        default=...,
        title="Window width",
        description="Width of the simulated window in pixel",
    )

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class WebPage(SQLModel):
    width: Optional[int] = Field(
        default=None,
        title="Page Width",
        description="Width of the simulated window in pixel",
    )
    height: Optional[int] = Field(
        default=None,
        title="Page Height",
        description="Height of the simulated window in pixel",
    )
    url: Optional[HttpUrl] = Field(
        default=None, title="Page url", description="Url of the analysed page"
    )


class Result(Ecoindex, PageMetrics, WebPage):
    date: Optional[datetime] = Field(
        default=None, title="Analysis datetime", description="Date of the analysis"
    )
    page_type: Optional[PageType] = Field(
        default=None,
        title="Page type",
        description="Is the type of the page, based ton the [opengraph type tag](https://ogp.me/#types)",
    )
