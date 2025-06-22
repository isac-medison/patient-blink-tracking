from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from use_cases.exceptions import EntityNotFoundError, ExternalError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_exception_handler(
            request: Request, exc: EntityNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(ExternalError)
    async def external_exception_handler(
            request: Request, exc: ExternalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something external went wrong. Please try again or contact tech specialist"},
        )

    @app.exception_handler(Exception)
    async def external_exception_handler(
            request: Request, exc: ExternalError
    ) -> JSONResponse:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something went wrong. Please try again or contact tech specialist"},
        )

