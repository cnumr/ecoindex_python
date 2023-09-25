from datetime import date, datetime
from os import getcwd
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import FileResponse

from ecoindex.api.database.engine import prisma
from ecoindex.api.utils.sorting import get_sort_parameters
from ecoindex.compute.ecoindex import get_ecoindex
from ecoindex.models import (
    ApiEcoindex,
    Ecoindex,
    PageApiEcoindexes,
    Version,
    example_ecoindex_not_found,
    example_file_not_found,
)

router = APIRouter(prefix="/ecoindex", tags=["Ecoindex"])


@router.get(
    name="Compute ecoindex",
    path="/",
    description=(
        "This returns the ecoindex computed based on the given parameters: "
        "DOM (number of DOM nodes), size (total size in Kb) and requests"
    ),
)
async def compute_ecoindex(
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
            default=..., description="Total size of the page in Kb", gt=0, example=109
        ),
    ],
    requests: Annotated[
        int,
        Query(
            default=..., description="Number of requests of the page", gt=0, example=5
        ),
    ],
) -> Ecoindex:
    return await get_ecoindex(dom=dom, size=size, requests=requests)


@router.get(
    name="Get ecoindex analysis list",
    path="/{version}/ecoindexes",
    response_model=PageApiEcoindexes,
    response_description="List of corresponding ecoindex results",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageApiEcoindexes},
        status.HTTP_404_NOT_FOUND: {"model": PageApiEcoindexes},
    },
    tags=["Ecoindex"],
    description=(
        "This returns a list of ecoindex analysis "
        "corresponding to query filters and the given version engine. "
        "The results are ordered by ascending date"
    ),
)
async def get_ecoindex_analysis_list(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    ),
    date_from: Annotated[
        date | None,
        Query(description="Start date of the filter elements (example: 2020-01-01)"),
    ] = None,
    date_to: Annotated[
        date | None,
        Query(description="End date of the filter elements  (example: 2020-01-01)"),
    ] = None,
    host: Annotated[
        str | None, Query(description="Host name you want to filter")
    ] = None,
    page: Annotated[int, Query(description="Page number", ge=1)] = 1,
    size: Annotated[
        int, Query(description="Number of elements per page", ge=1, le=100)
    ] = 50,
    sort: Annotated[
        list[str],
        Query(
            description=(
                "You can sort results using this param with the format "
                "`sort=param1:asc&sort=param2:desc`"
            )
        ),
    ] = ["date:desc"],
) -> PageApiEcoindexes:
    where = {"version": version.get_version_number(), "date": {}}
    if date_from:
        where["date"]["gte"] = datetime.combine(date_from, datetime.min.time())
    if date_to:
        where["date"]["lte"] = datetime.combine(date_to, datetime.min.time())
    if host:
        where["host"] = {"contains": host}

    print(where)

    ecoindexes = await prisma.ecoindex.find_many(
        skip=(page - 1) * size,
        take=size,
        where=where,
        order=[
            {param.clause: param.sort}
            for param in await get_sort_parameters(sort, ApiEcoindex)
        ],
    )

    total = await prisma.ecoindex.count(where=where)

    return PageApiEcoindexes(
        items=[ApiEcoindex(**ecoindex.model_dump()) for ecoindex in ecoindexes],
        total=total,
        page=page,
        size=size,
    )


@router.get(
    name="Get ecoindex analysis by id",
    path="/{version}/ecoindexes/{id}",
    response_model=ApiEcoindex,
    response_description="Get one ecoindex result by its id",
    responses={status.HTTP_404_NOT_FOUND: example_ecoindex_not_found},
    description="This returns an ecoindex given by its unique identifier",
)
async def get_ecoindex_analysis_by_id(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    ),
    id: UUID = Path(
        default=..., description="Unique identifier of the ecoindex analysis"
    ),
) -> ApiEcoindex:
    ecoindex = await prisma.ecoindex.find_first(
        where={"id": str(id), "version": version.get_version_number()}
    )

    if not ecoindex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {id} not found for version {version.value}",
        )

    return ecoindex


@router.get(
    name="Get screenshot",
    path="/{version}/ecoindexes/{id}/screenshot",
    description="This returns the screenshot of the webpage analysis if it exists",
    responses={status.HTTP_404_NOT_FOUND: example_file_not_found},
)
async def get_screenshot(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    ),
    id: UUID = Path(
        default=..., description="Unique identifier of the ecoindex analysis"
    ),
):
    return FileResponse(
        path=f"{getcwd()}/ecoindex/api/screenshots/{version.value}/{id}.webp",
        filename=f"{id}.webp",
        content_disposition_type="inline",
        media_type="image/webp",
    )
