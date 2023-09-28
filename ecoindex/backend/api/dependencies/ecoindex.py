from typing import Annotated, Dict
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

    def get_where_clause(self) -> Dict:
        return {
            "version": self.version.get_version_number(),
            "id": str(self.id),
        }


class EcoindexComputeParams:
    def __init__(
        self,
        dom: Annotated[
            int,
            Query(
                default=...,
                description="Number of DOM nodes of the page",
                gt=0,
                example=204,
            ),
        ],
        size: Annotated[
            float,
            Query(
                default=...,
                description="Total size of the page in Kb",
                gt=0,
                example=109,
            ),
        ],
        requests: Annotated[
            int,
            Query(
                default=...,
                description="Number of requests of the page",
                gt=0,
                example=5,
            ),
        ],
    ) -> None:
        self.dom = dom
        self.size = size
        self.requests = requests
