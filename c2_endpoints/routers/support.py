from fastapi import APIRouter, Form
from typing import Annotated

router = APIRouter(
    tags=["support"]
)


@router.post("/support-ticket")
async def create_support_ticket(
    title: Annotated[str, Form()],
    message: Annotated[str, Form()]
):
    return {"title": title, "message": message}
