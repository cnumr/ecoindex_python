from typing import List

from ecoindex.backend.api.dependencies import CommonListParams, PaginationParams
from ecoindex.backend.database.engine import prisma


async def list_hosts_db(
    parameters: CommonListParams, pagination: PaginationParams
) -> List[str]:
    hosts = await prisma.ecoindex.group_by(
        by=["host"],
        skip=(pagination.page - 1) * pagination.size,
        take=pagination.size,
        where=parameters.get_where_clause(),
        order={"host": "asc"},
        count=True,
    )

    return [host["host"] for host in hosts]
