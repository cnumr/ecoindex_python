from datetime import datetime
from os import getcwd
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse

from ecoindex.backend.api.dependencies.ecoindex import (
    CommonEcoindexDetailParams,
    CommonEcoindexListParams,
)
from ecoindex.backend.api.dependencies.pagination import PaginationParams
from ecoindex.backend.api.utils.sorting import get_sort_parameters
from ecoindex.backend.database.engine import prisma
from ecoindex.compute.ecoindex import get_ecoindex
from ecoindex.models import (
    ApiEcoindex,
    Ecoindex,
    PageApiEcoindexes,
    Requests,
    example_ecoindex_not_found,
    example_file_not_found,
)

router = APIRouter(prefix="/ecoindex", tags=["Ecoindex"])


@router.get(
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
    path="/{version}/ecoindexes",
    response_model=PageApiEcoindexes,
    response_description="List of corresponding ecoindex results",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageApiEcoindexes},
        status.HTTP_404_NOT_FOUND: {"model": PageApiEcoindexes},
    },
    description=(
        "This returns a list of ecoindex analysis "
        "corresponding to query filters and the given version engine. "
        "The results are ordered by ascending date"
    ),
)
async def get_ecoindex_analysis_list(
    params: CommonEcoindexListParams = Depends(CommonEcoindexListParams),
    pagination: PaginationParams = Depends(PaginationParams),
) -> PageApiEcoindexes:
    # TODO: Refactor this to use a repository
    where = {"version": params.version.get_version_number(), "date": {}}
    if params.date_from:
        where["date"]["gte"] = datetime.combine(params.date_from, datetime.min.time())
    if params.date_to:
        where["date"]["lte"] = datetime.combine(params.date_to, datetime.min.time())
    if params.host:
        where["host"] = {"contains": params.host}

    ecoindexes = await prisma.ecoindex.find_many(
        skip=(pagination.page - 1) * pagination.size,
        take=pagination.size,
        where=where,
        order=[
            {param.clause: param.sort}
            for param in await get_sort_parameters(pagination.sort, ApiEcoindex)
        ],
    )

    total = await prisma.ecoindex.count(where=where)

    return PageApiEcoindexes(
        items=[ApiEcoindex(**ecoindex.model_dump()) for ecoindex in ecoindexes],
        total=total,
        page=pagination.page,
        size=pagination.size,
    )


@router.get(
    path="/{version}/ecoindexes/{id}",
    response_model=ApiEcoindex,
    response_description="Get one ecoindex result by its id",
    responses={status.HTTP_404_NOT_FOUND: example_ecoindex_not_found},
    description="This returns an ecoindex given by its unique identifier",
)
async def get_ecoindex_analysis_by_id(
    params: CommonEcoindexDetailParams = Depends(CommonEcoindexDetailParams),
) -> ApiEcoindex:
    ecoindex = await prisma.ecoindex.find_first(
        where={
            "id": str(params.id),
            "version": params.version.get_version_number(),
        }
    )

    if not ecoindex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {params.id} not found for version {params.version.value}",
        )

    return ecoindex


@router.get(
    path="/{version}/ecoindexes/{id}/screenshot",
    description="This returns the screenshot of the webpage analysis if it exists",
    responses={status.HTTP_404_NOT_FOUND: example_file_not_found},
)
async def get_ecoindex_screenshot(
    params: CommonEcoindexDetailParams = Depends(CommonEcoindexDetailParams),
) -> FileResponse:
    return FileResponse(
        path=f"{getcwd()}/ecoindex/api/screenshots/{params.version.value}/{params.id}.webp",
        filename=f"{params.id}.webp",
        content_disposition_type="inline",
        media_type="image/webp",
    )


@router.get(
    path="/{version}/ecoindexes/{id}/requests",
    description="This returns the requests details of the webpage analysis",
    responses={status.HTTP_404_NOT_FOUND: example_ecoindex_not_found},
)
async def get_ecoindex_requests_details(
    params: CommonEcoindexDetailParams = Depends(CommonEcoindexDetailParams),
) -> List[Requests]:
    ecoindex = await prisma.ecoindex.find_first(
        where={
            "id": str(params.id),
            "version": params.version.get_version_number(),
        },
        include={"requests_details": True},
    )

    if not ecoindex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {params.id} not found for version {params.version.value}",
        )

    return [
        Requests(url=request.url, size=request.size, type=request.type)
        for request in ecoindex.requests_details
    ]
