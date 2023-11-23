from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api import deps
from src.db import crud
from src.db import schemas, models

router = APIRouter()


@router.get("/history", response_model=List[schemas.CartItem])
def read_history(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve history items.

    Requires authentication.
    """
    items = crud.get_cart_items(
        db=db, user_email=current_user.email, skip=skip, limit=limit, has_purchased=True
    )
    return items


@router.get("/cart", response_model=List[schemas.CartItem])
def read_cart(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cart items.

    Requires authentication.
    """
    items = crud.get_cart_items(
        db=db, user_email=current_user.email, skip=skip, limit=limit, has_purchased=False
    )
    return items


@router.get("/{id}", response_model=schemas.CartItem)
def read_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get an item from cart or history by ID.

    Requires authentication.
    """
    item = crud.get_cart_item(db=db, item_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user.email != current_user.email:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=schemas.CartItem)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.CartItemCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Add a new item to cart, or to history if has_purchased is True.

    Requires authentication.
    """
    item = crud.create_cart_item(db=db, item=item_in, user_email=current_user.email)
    return item


@router.put("/{id}", response_model=schemas.CartItem)
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        item_id: int,
        item_in: schemas.CartItemUpdate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Move an item from cart to history if has_purchased is True, and vice versa.

    Requires authentication.
    """
    item = crud.get_cart_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user.email != current_user.email:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.update_cart_item(db=db, item=item_in, item_id=item_id)
    return item

# @router.delete("/{id}", response_model=schemas.CartItem)
# def delete_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     item_id: int,
#     current_user: models.User = Depends(deps.get_current_user),
# ) -> Any:
#     """
#     Delete an item.
#     """
#     item = crud.get_cart_item(db=db, item_id=item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if item.user.email != current_user.email:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.delete_cart_item(db=db, item_id=item_id)
#     return item
