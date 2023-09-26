from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import Path, Query

from ecoindex.models import Version


class CommonEcoindexDetailParams:
    def __init__(
        self,
        version: Annotated[
            Version,
            Path(
                default=...,
                title="Engine version",
                description="Engine version used to run the analysis (v0 or v1)",
                example=Version.v1.value,
            ),
        ],
        id: Annotated[
            UUID,
            Path(default=..., description="Unique identifier of the ecoindex analysis"),
        ],
    ) -> None:
        self.version = version
        self.id = id


class CommonEcoindexListParams:
    def __init__(
        self,
        version: Version = Path(
            default=...,
            title="Engine version",
            description="Engine version used to run the analysis (v0 or v1)",
            example=Version.v1.value,
        ),
        date_from: Annotated[
            date | None,
            Query(
                description="Start date of the filter elements (example: 2020-01-01)"
            ),
        ] = None,
        date_to: Annotated[
            date | None,
            Query(description="End date of the filter elements  (example: 2020-01-01)"),
        ] = None,
        host: Annotated[
            str | None, Query(description="Host name you want to filter")
        ] = None,
    ):
        self.date_from = date_from
        self.date_to = date_to
        self.host = host
        self.version = version
