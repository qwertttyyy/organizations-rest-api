from typing import Sequence

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import verify_api_key, get_session
from app.schemas.activity import ActivityResponse
from app.schemas.building import BuildingResponse
from app.schemas.organization import OrganizationResponse
from app.services.organization_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(verify_api_key)],
)


def to_response(objs) -> list[OrganizationResponse]:
    """Преобразует ORM-объекты в Pydantic-схемы ответа.

    Args:
        objs: Последовательность ORM-организаций.

    Returns:
        Список схем ответа.
    """
    result: list[OrganizationResponse] = []
    for o in objs:
        br = BuildingResponse(
            id=o.building.id,
            address=o.building.address,
            latitude=o.building.latitude,
            longitude=o.building.longitude,
        )
        acts = [
            ActivityResponse(
                id=a.id, name=a.name, parent_id=a.parent_id, level=a.level
            )
            for a in o.activities
        ]
        phones = [p.phone_number for p in o.phones]
        result.append(
            OrganizationResponse(
                id=o.id,
                name=o.name,
                building=br,
                activities=acts,
                phones=phones,
            )
        )
    return result


@router.get(
    "/by-building/{building_id}", response_model=list[OrganizationResponse]
)
async def organizations_by_building(
    building_id: int = Path(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Возвращает организации в заданном здании.

    Args:
        building_id: Идентификатор здания.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.get_by_building(
        building_id=building_id, skip=skip, limit=limit
    )
    return to_response(objs)


@router.get(
    "/by-activity/{activity_id}", response_model=list[OrganizationResponse]
)
async def organizations_by_activity(
    activity_id: int = Path(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Возвращает организации по виду деятельности.

    Args:
        activity_id: Идентификатор деятельности.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.get_by_activity(
        activity_id=activity_id, skip=skip, limit=limit
    )
    return to_response(objs)


@router.get("/in-radius", response_model=list[OrganizationResponse])
async def organizations_in_radius(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: float = Query(..., gt=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Возвращает организации в радиусе, метры.

    Args:
        lat: Широта центра.
        lon: Долгота центра.
        radius: Радиус в метрах.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.in_radius(
        lat=lat, lon=lon, radius_m=radius, skip=skip, limit=limit
    )
    return to_response(objs)


@router.get("/in-area", response_model=list[OrganizationResponse])
async def organizations_in_area(
    lat1: float = Query(..., ge=-90, le=90),
    lon1: float = Query(..., ge=-180, le=180),
    lat2: float = Query(..., ge=-90, le=90),
    lon2: float = Query(..., ge=-180, le=180),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Возвращает организации в прямоугольной области.

    Args:
        lat1: Нижняя широта.
        lon1: Левая долгота.
        lat2: Верхняя широта.
        lon2: Правая долгота.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.in_area(
        lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2, skip=skip, limit=limit
    )
    return to_response(objs)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def organization_detail(
    organization_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
) -> OrganizationResponse:
    """Возвращает детальную информацию об организации.

    Args:
        organization_id: Идентификатор организации.
        session: Асинхронная сессия.

    Returns:
        Организация со связями.
    """
    service = OrganizationService(session)
    o = await service.get_detail(organization_id=organization_id)
    br = BuildingResponse(
        id=o.building.id,
        address=o.building.address,
        latitude=o.building.latitude,
        longitude=o.building.longitude,
    )
    acts = [
        ActivityResponse(
            id=a.id, name=a.name, parent_id=a.parent_id, level=a.level
        )
        for a in o.activities
    ]
    phones = [p.phone_number for p in o.phones]
    return OrganizationResponse(
        id=o.id, name=o.name, building=br, activities=acts, phones=phones
    )


@router.get(
    "/search/by-activity-tree/{activity_id}",
    response_model=list[OrganizationResponse],
)
async def organizations_by_activity_tree(
    activity_id: int = Path(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Ищет организации по всему поддереву деятельности.

    Args:
        activity_id: Идентификатор корневого вида.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.by_activity_tree(
        activity_id=activity_id, skip=skip, limit=limit
    )
    return to_response(objs)


@router.get("/search", response_model=list[OrganizationResponse])
async def organizations_search(
    name: str = Query(..., min_length=1, max_length=255),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> Sequence[OrganizationResponse]:
    """Ищет организации по названию.

    Args:
        name: Фрагмент названия.
        skip: Смещение.
        limit: Лимит.
        session: Асинхронная сессия.

    Returns:
        Список организаций.
    """
    service = OrganizationService(session)
    objs = await service.search_by_name(name=name, skip=skip, limit=limit)
    return to_response(objs)
