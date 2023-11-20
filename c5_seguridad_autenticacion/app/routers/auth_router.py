from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database import DB_DEPENDECY
from app.models.user_model import User
from app.schemas.user_schema import CreateUserRequest, UserInfo
from app.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_hashed_password,
    verify_password,
)
from app.schemas.auth_schema import TokenSchema


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

OAUTH_DEPENDENCY = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=UserInfo)
async def create_user(db: DB_DEPENDECY, user_data: CreateUserRequest):
    user = db.query(User).filter(User.email==user_data.email).first()
    print(user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is registered"
        )

    user_model = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=get_hashed_password(user_data.password),
    )
    db.add(user_model)
    db.commit()

    return user_model


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def login(form_data: OAUTH_DEPENDENCY, db: DB_DEPENDECY):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = db.query(User).filter_by(email=form_data.username).first()
    if not user:
        raise credentials_exception

    verified_user = verify_password(form_data.password, user.hashed_password)
    if not verified_user:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

