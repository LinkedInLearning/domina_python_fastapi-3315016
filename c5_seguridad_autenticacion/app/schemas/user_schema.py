from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateUserRequest(UserInfo):
    password:str
