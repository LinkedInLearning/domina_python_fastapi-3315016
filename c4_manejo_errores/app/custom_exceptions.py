from fastapi import Request, status
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Something went wrong with {exc.name}"},
    )
