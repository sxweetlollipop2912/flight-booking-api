from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from db import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve tickets.
    """
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets
