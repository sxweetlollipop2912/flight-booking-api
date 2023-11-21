from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from db import models
from db import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.get_user(db, user_email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.create_user(db, user=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
