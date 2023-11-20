from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import UserInfo


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserInfo)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
