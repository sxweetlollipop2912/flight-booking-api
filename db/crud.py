from typing import Optional

from sqlalchemy.orm import Session

from core import security
from db import models
from db import schemas
from db.db_mock_tickets import db_tickets


def get_user(db: Session, user_email: str):
    return db.query(models.User).get(user_email)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, *, email: str, password: str) -> Optional[models.User]:
    user = get_user(db, user_email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return [models.Ticket(**ticket) for ticket in db_tickets[skip:skip + limit]]
    # return (db.query(models.Ticket)
    #         .offset(skip)
    #         .limit(limit)
    #         .all())


def get_ticket(db: Session, ticket_id: int):
    ticket = next((ticket for ticket in db_tickets if ticket.get("id") == ticket_id), None)
    return models.Ticket(**ticket)
    # return db.query(models.Ticket).get(ticket_id)


def create_tickets(db: Session, ticket: schemas.TicketCreate):
    db_ticket = {
        "id": len(db_tickets) + 1,
        "origin": ticket.origin,
        "destination": ticket.destination,
        "depart_time": ticket.depart_time,
        "arrive_time": ticket.arrive_time,
        "price": ticket.price
    }
    db_tickets.append(db_ticket)
    return models.Ticket(**db_ticket)
    # db_ticket = models.Ticket(
    #     origin=ticket.origin,
    #     destination=ticket.destination,
    #     depart_time=ticket.depart_time,
    #     arrive_time=ticket.arrive_time,
    #     price=ticket.price
    # )
    # db.add(db_ticket)
    # db.commit()
    # db.refresh(db_ticket)
    # return db_ticket


def get_cart_item(db: Session, item_id: int) -> models.CartItem:
    return db.query(models.CartItem).get(item_id)


def get_cart_items(db: Session, user_email: str, skip: int = 0, limit: int = 100, has_purchased: Optional[bool] = None):
    return (db.query(models.CartItem)
            .filter(models.CartItem.user_email == user_email,
                    (has_purchased is None
                     or models.CartItem.has_purchased == has_purchased))
            .offset(skip)
            .limit(limit)
            .all())


def create_cart_item(db: Session, item: schemas.CartItemCreate, user_email: str):
    db_item = models.CartItem(has_purchased=item.has_purchased, ticket_id=item.ticket_id, user_email=user_email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_cart_item(db: Session, item: schemas.CartItemUpdate, item_id: int):
    db_item = get_cart_item(db, item_id)
    db_item.has_purchased = item.has_purchased
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_cart_item(db: Session, item_id: int):
    db_item = db.query(models.CartItem).get(item_id)
    db.delete(db_item)
    db.commit()
    return db_item
