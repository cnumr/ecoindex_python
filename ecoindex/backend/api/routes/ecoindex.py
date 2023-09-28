from os import getcwd
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import FileResponse

from ecoindex.backend.api.dependencies import (
    CommonEcoindexDetailParams,
    CommonListParams,
    EcoindexComputeParams,
)
from ecoindex.backend.api.dependencies.common import SortParams
from ecoindex.backend.api.dependencies.pagination import PaginationParams
from ecoindex.backend.database.repository.ecoindex import (
    count_ecoindexes_db,
    get_ecoindex_by_id_db,
    get_ecoindex_requests_details_db,
    list_ecoindexes_db,
)
from ecoindex.compute.ecoindex import get_ecoindex
from ecoindex.models import (
    ApiEcoindex,
    Ecoindex,
    PageApiEcoindexes,
    example_ecoindex_not_found,
    example_file_not_found,
    example_page_listing_empty,
)
from ecoindex.models.compute import Request

router = APIRouter(prefix="/ecoindex", tags=["Ecoindex"])


@router.get(
    path="/",
    description="""
    This returns the ecoindex computed based on the given parameters: 
    DOM (number of DOM nodes), size (total size in Kb) and requests
    """,
)
async def compute_ecoindex(
    params: Annotated[EcoindexComputeParams, Depends()],
) -> Ecoindex:
    return await get_ecoindex(
        dom=params.dom, size=params.size, requests=params.requests
    )


@router.get(
    path="/{version}/ecoindexes",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageApiEcoindexes},
        status.HTTP_204_NO_CONTENT: example_page_listing_empty,
    },
    description="""
    This returns a list of ecoindex analysis 
    corresponding to query filters and the given version engine. 
    The results are ordered by ascending date
    """,
)
async def get_ecoindex_analysis_list(
    params: Annotated[CommonListParams, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortParams, Depends()],
    response: Response,
) -> PageApiEcoindexes:
    ecoindexes = await list_ecoindexes_db(
        pagination=pagination, parameters=params, sorting=sorting
    )

    total = await count_ecoindexes_db(parameters=params)

    if total == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    if total > len(ecoindexes):
        response.status_code = status.HTTP_206_PARTIAL_CONTENT

    return PageApiEcoindexes(
        items=ecoindexes,
        total=total,
        page=pagination.page,
        size=pagination.size,
    )


@router.get(
    path="/{version}/ecoindexes/{id}",
    responses={status.HTTP_404_NOT_FOUND: example_ecoindex_not_found},
    description="This returns an ecoindex given by its unique identifier",
)
async def get_ecoindex_analysis_by_id(
    params: Annotated[CommonEcoindexDetailParams, Depends()]
) -> ApiEcoindex:
    ecoindex = await get_ecoindex_by_id_db(parameters=params)

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
    params: Annotated[CommonEcoindexDetailParams, Depends()]
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
    params: Annotated[CommonEcoindexDetailParams, Depends()]
) -> List[Request]:
    ecoindex_exists, requests = await get_ecoindex_requests_details_db(
        parameters=params
    )

    if not ecoindex_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {params.id} not found for version {params.version.value}",
        )

    return requests
