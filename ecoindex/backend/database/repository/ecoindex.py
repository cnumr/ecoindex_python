from typing import List, Tuple

from ecoindex.backend.api.dependencies import (
    CommonEcoindexDetailParams,
    CommonListParams,
)
from ecoindex.backend.api.dependencies.common import SortParams
from ecoindex.backend.api.dependencies.pagination import PaginationParams
from ecoindex.backend.database.engine import prisma
from ecoindex.models.api import ApiEcoindex
from ecoindex.models.compute import Ecoindex, Request


async def list_ecoindexes_db(
    pagination: PaginationParams, parameters: CommonListParams, sorting: SortParams
) -> List[ApiEcoindex]:
    ecoindexes = await prisma.ecoindex.find_many(
        skip=(pagination.page - 1) * pagination.size,
        take=pagination.size,
        where=parameters.get_where_clause(),
        order=sorting.get_sort_clause(model=ApiEcoindex),
    )

    return [ApiEcoindex(**ecoindex.model_dump()) for ecoindex in ecoindexes]


async def count_ecoindexes_db(parameters: CommonListParams) -> int:
    return await prisma.ecoindex.count(where=parameters.get_where_clause())


async def get_ecoindex_by_id_db(
    parameters: CommonEcoindexDetailParams,
) -> Ecoindex | None:
    return await prisma.ecoindex.find_first(
        where={
            "id": str(parameters.id),
            "version": parameters.version.get_version_number(),
        }
    )


async def get_ecoindex_requests_details_db(
    parameters: CommonEcoindexDetailParams,
) -> Tuple[bool, List[Request]]:
    ecoindex = await prisma.ecoindex.find_first(
        where=parameters.get_where_clause(),
        include={"requests_details": True},
    )

    if ecoindex is None:
        return False, []

    return True, [
        Request(url=request.url, size=request.size, type=request.type)
        for request in ecoindex.requests_details
    ]
