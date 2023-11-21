from fastapi import APIRouter

from api.endpoints import login, users
from api.endpoints import cart_items, tickets

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(cart_items.router, prefix="/items", tags=["items"])
