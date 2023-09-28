from typing import Annotated

from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        page: Annotated[int, Query(description="Page number", ge=1)] = 1,
        size: Annotated[
            int, Query(description="Number of elements per page", ge=1, le=100)
        ] = 50,
    ) -> None:
        self.page = page
        self.size = size
