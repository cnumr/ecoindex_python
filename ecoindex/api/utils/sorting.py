import re

from fastapi import HTTPException, status
from pydantic import BaseModel

from ecoindex.models.sort import Sort


async def get_sort_parameters(query_params: list[str], model: BaseModel) -> list[Sort]:
    """Get sort parameters from query parameters

    Args:
        query_params (list[str]): list of query parameters
        model (BaseModel): pydantic model

    Raises:
        HTTPException: if query parameters are not valid

    Returns:
        list[Sort]: list of Sort objects
    """

    validation_error = []
    result = []

    for query_param in query_params:
        pattern = re.compile("^\w+:(asc|desc)$")

        if not re.fullmatch(pattern, query_param):
            validation_error.append(
                {
                    "loc": ["query", "sort", query_param],
                    "message": "this parameter does not respect the sort format",
                    "type": "value_error.sort",
                }
            )
            continue

        sort_params = query_param.split(":")

        if sort_params[0] not in model.__fields__:
            validation_error.append(
                {
                    "loc": ["query", "sort", sort_params[0]],
                    "message": "this parameter does not exist",
                    "type": "value_error.sort",
                }
            )

        result.append(Sort(clause=sort_params[0], sort=sort_params[1]))

    if validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=validation_error
        )

    return result
