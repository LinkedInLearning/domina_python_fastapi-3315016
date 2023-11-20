from jose import jwt
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import DB_DEPENDECY
from app.models.user_model import User
from app.schemas.auth_schema import TokenUserSchema
from app.utils import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB_DEPENDECY):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise credentials_exception

        token_data = TokenUserSchema(email=email)
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(User).filter_by(email=token_data.email).first()
    if not user:
        raise credentials_exception

    return user
