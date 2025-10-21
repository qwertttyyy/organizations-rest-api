from typing import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import verify_api_key, get_session
from app.schemas.building import BuildingResponse
from app.services.building_service import BuildingService

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("", response_model=list[BuildingResponse])
async def list_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[BuildingResponse]:
    """Возвращает список зданий с пагинацией.

    Args:
        skip: Смещение.
        limit: Лимит записей.
        session: Асинхронная сессия.

    Returns:
        Список зданий.
    """
    service = BuildingService(session)
    objs = await service.list(skip=skip, limit=limit)
    return [
        BuildingResponse(
            id=o.id,
            address=o.address,
            latitude=o.latitude,
            longitude=o.longitude,
        )
        for o in objs
    ]
