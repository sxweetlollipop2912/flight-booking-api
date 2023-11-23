from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import deps
from core import security
from core.config import settings
from db import crud, schemas

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests

    For convenience, if email does not exist, this endpoint will register a new user
        with the provided email and password.

    Note that "username" must be an email.
    """
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        user = crud.get_user(db, user_email=form_data.username)
        if user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        else:
            user = crud.create_user(db, user=schemas.UserCreate(
                email=form_data.username,
                password=form_data.password
            ))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
