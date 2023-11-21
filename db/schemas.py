from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class TicketBase(BaseModel):
    origin: str
    destination: str
    depart_time: datetime
    arrive_time: datetime
    price: int


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int

    class Config:
        orm_mode = True


class CartItemBase(BaseModel):
    has_purchased: bool = False


class CartItemCreate(CartItemBase):
    ticket_id: int


class CartItemUpdate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int
    user_email: EmailStr
    ticket_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    items: list[CartItem] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
