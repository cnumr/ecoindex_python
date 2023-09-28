import re
from datetime import date, datetime
from typing import Annotated, Dict

from fastapi import HTTPException, Path, Query, status
from pydantic import BaseModel

from ecoindex.models import Sort, Version


class CommonListParams:
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
        date_from: Annotated[
            date | None,
            Query(
                description="Start date of the filter elements (example: 2020-01-01)"
            ),
        ] = None,
        date_to: Annotated[
            date | None,
            Query(description="End date of the filter elements  (example: 2020-01-01)"),
        ] = None,
        host: Annotated[
            str | None, Query(description="Host name you want to filter")
        ] = None,
    ):
        self.date_from = date_from
        self.date_to = date_to
        self.host = host
        self.version = version

    def get_where_clause(self) -> Dict:
        where = {"version": self.version.get_version_number(), "date": {}}

        if self.date_from:
            where["date"]["gte"] = datetime.combine(self.date_from, datetime.min.time())
        if self.date_to:
            where["date"]["lte"] = datetime.combine(self.date_to, datetime.min.time())
        if self.host:
            where["host"] = {"contains": self.host}

        return where


class SortParams:
    def __init__(
        self,
        sort: Annotated[
            list[str],
            Query(
                description=(
                    "You can sort results using this param with the format "
                    "`sort=param1:asc&sort=param2:desc`"
                )
            ),
        ] = ["date:desc"],
    ):
        self.sort = sort

    def get_sort_clause(self, model: BaseModel) -> list[Sort]:
        """Get sort parameters from query parameters

        Args:
            model (BaseModel): pydantic model

        Raises:
            HTTPException: if query parameters are not valid

        Returns:
            list[Sort]: list of Sort objects
        """

        validation_error = []
        result = []

        for query_param in self.sort:
            pattern = re.compile("^\w+:(asc|desc)$")

            if not re.fullmatch(pattern, query_param):
                validation_error.append(
                    {
                        "loc": ["query", "sort", query_param],
                        "message": (
                            "this parameter does not respect the sort "
                            "format (example: `sort=date:asc`)"
                        ),
                        "type": "value_error.sort",
                    }
                )
                continue

            sort_params = query_param.split(":")

            if sort_params[0] not in model.__fields__:
                validation_error.append(
                    {
                        "loc": ["query", "sort", sort_params[0]],
                        "message": (
                            "this parameter does not exist "
                            f"for the model {model.__name__}"
                        ),
                        "type": "value_error.sort",
                    }
                )

            result.append({sort_params[0]: sort_params[1]})

        if validation_error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=validation_error,
            )

        return result
