from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.organizations import router as organizations_router
from app.routers.buildings import router as buildings_router
from app.routers.activities import router as activities_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="REST API для справочника Организаций.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(organizations_router)
app.include_router(buildings_router)
app.include_router(activities_router)
