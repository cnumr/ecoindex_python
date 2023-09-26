from datetime import datetime

from fastapi import APIRouter, Depends, Path, status

from ecoindex.backend.api.dependencies.ecoindex import CommonEcoindexListParams
from ecoindex.backend.api.dependencies.pagination import PaginationParams
from ecoindex.backend.database.engine import prisma
from ecoindex.models import Host, PageHosts, Version, example_daily_limit_response

router = APIRouter(tags=["Hosts"], prefix="/{version}/hosts")


@router.get(
    name="Get host list",
    path="/",
    response_model=PageHosts,
    response_description="List ecoindex hosts",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageHosts},
        status.HTTP_404_NOT_FOUND: {"model": PageHosts},
    },
    description="""
    This returns a list of hosts that 
    ran an ecoindex analysis order by most request made
    """,
)
async def get_host_list(
    params: CommonEcoindexListParams = Depends(CommonEcoindexListParams),
    pagination: PaginationParams = Depends(PaginationParams),
) -> PageHosts:
    where = {"version": params.version.get_version_number(), "date": {}}
    if params.date_from:
        where["date"]["gte"] = datetime.combine(params.date_from, datetime.min.time())
    if params.date_to:
        where["date"]["lte"] = datetime.combine(params.date_to, datetime.min.time())
    if params.host:
        where["host"] = {"contains": params.host}

    hosts = await prisma.ecoindex.group_by(
        by=["host"],
        skip=(pagination.page - 1) * pagination.size,
        take=pagination.size,
        where=where,
        order={"host": "asc"},
        count=True,
    )

    # response.status_code = await get_status_code(items=hosts, total=total_hosts)
    # TODO: apply where to count
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
        items=[host["host"] for host in hosts],
        total=count[0]["count"],
        page=pagination.page,
        size=pagination.size,
    )


@router.get(
    name="Get host details",
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
async def get_daily_remaining(
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
    return Host(name=host, remaining_daily_requests=0, total_count=1)
