from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, plants, users_plants, detector

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(plants.router, prefix="/plants", tags=["plants"])
api_router.include_router(users_plants.router, prefix="/users-plants", tags=["users-plants"])
api_router.include_router(detector.router, prefix="/detector", tags=["detector"])

