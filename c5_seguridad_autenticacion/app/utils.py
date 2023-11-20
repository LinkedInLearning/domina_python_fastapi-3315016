from datetime import datetime, timedelta
from typing import Union
from jose import jwt
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = "8757d580e059b565dea8d85e24deaf2642d3c1dce1ac2911b5e6ebd5e050f000"


def get_hashed_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
