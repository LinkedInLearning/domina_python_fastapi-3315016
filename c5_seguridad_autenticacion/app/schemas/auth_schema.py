from typing import Union
from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenUserSchema(BaseModel):
    email: Union[str, None] = None
