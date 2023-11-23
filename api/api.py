from fastapi import APIRouter

from api.endpoints import items, tickets
from api.endpoints import login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
