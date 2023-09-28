from fastapi import APIRouter, Depends, Path, status

from ecoindex.backend.api.dependencies import CommonListParams, PaginationParams
from ecoindex.backend.database.engine import prisma
from ecoindex.backend.database.repository.host import list_hosts_db
from ecoindex.models import (
    Host,
    PageHosts,
    Version,
    example_daily_limit_response,
    example_page_listing_empty,
)

router = APIRouter(tags=["Hosts"], prefix="/{version}/hosts")


@router.get(
    path="/",
    response_model=PageHosts,
    response_description="List ecoindex hosts",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageHosts},
        status.HTTP_204_NO_CONTENT: example_page_listing_empty,
    },
    description="""
    This returns a list of hosts that 
    ran an ecoindex analysis order by most request made
    """,
)
async def get_host_list(
    params: CommonListParams = Depends(CommonListParams),
    pagination: PaginationParams = Depends(PaginationParams),
) -> PageHosts:
    hosts = await list_hosts_db(parameters=params, pagination=pagination)

    # TODO: create repository
    count = await prisma.query_raw(
        """
        SELECT COUNT(DISTINCT host) as count 
        FROM api_ecoindex 
        WHERE version = ?
        """,
        params.version.get_version_number(),
    )

    return PageHosts(
        items=hosts,
        total=count[0]["count"],
        page=pagination.page,
        size=pagination.size,
    )


@router.get(
    path="/{host}",
    response_description="Host details",
    responses={
        status.HTTP_200_OK: {"model": Host},
        status.HTTP_404_NOT_FOUND: {"model": Host},
        status.HTTP_429_TOO_MANY_REQUESTS: example_daily_limit_response,
    },
    description="""
    This returns the details of a host. If no no quota is set, 
    remaining_daily_requests will be null
    """,
)
async def get_host_details(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    ),
    host: str = Path(
        default=...,
        title="Host name",
        description="Host name used to run the analysis",
        example="www.ecoindex.fr",
    ),
) -> Host:
    # TODO: Implement repository
    return Host(name=host, remaining_daily_requests=0, total_count=1)
