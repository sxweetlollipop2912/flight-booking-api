from fastapi import APIRouter

from src.api.endpoints import tickets, items, login
from src.api.endpoints import users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
