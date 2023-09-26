from typing import Annotated

from fastapi import Query


class PaginationParams:
    def __init__(
        self,
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
    ) -> None:
        self.page = page
        self.size = size
        self.sort = sort
