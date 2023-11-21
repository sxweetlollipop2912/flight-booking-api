from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)

    # Relationships
    cart_items = relationship("CartItem", back_populates="user")


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    depart_time = Column(String, nullable=False)
    arrive_time = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(origin, destination, depart_time, arrive_time),
    )


class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True)
    has_purchased = Column(Boolean, default=False)

    user_email = Column(String, ForeignKey("user.email"))
    # ticket_id = Column(Integer, ForeignKey("ticket.id"))
    ticket_id = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="cart_items")
