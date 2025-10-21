from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_organization import organization_crud
from app.models.organization import Organization
from app.utils.geo import bounding_box_for_radius, filter_by_radius
from app.services.activity_service import ActivityService


class OrganizationService:
    """Сервис для работы с организациями и геопоиском."""

    def __init__(self, session: AsyncSession) -> None:
        """Создает экземпляр сервиса.

        Args:
            session: Асинхронная сессия БД.
        """
        self.session = session

    async def get_by_building(
        self, building_id: int, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Возвращает организации по зданию.

        Args:
            building_id: Идентификатор здания.
            skip: Смещение.
            limit: Лимит записей.

        Returns:
            Последовательность организаций.
        """
        return await organization_crud.by_building(
            self.session, building_id=building_id, skip=skip, limit=limit
        )

    async def get_by_activity(
        self, activity_id: int, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Возвращает организации по виду деятельности.

        Args:
            activity_id: Идентификатор деятельности.
            skip: Смещение.
            limit: Лимит записей.

        Returns:
            Последовательность организаций.
        """
        return await organization_crud.by_activity(
            self.session, activity_id=activity_id, skip=skip, limit=limit
        )

    async def get_detail(self, organization_id: int) -> Organization:
        """Возвращает детальную информацию об организации.

        Args:
            organization_id: Идентификатор организации.

        Returns:
            Организация с загруженными связями.

        Raises:
            HTTPException: Если организация не найдена.
        """
        obj = await organization_crud.get_detail(self.session, organization_id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )
        return obj

    async def search_by_name(
        self, name: str, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Ищет организации по фрагменту названия.

        Args:
            name: Фрагмент.
            skip: Смещение.
            limit: Лимит.

        Returns:
            Последовательность организаций.
        """
        return await organization_crud.search_by_name(
            self.session, name=name, skip=skip, limit=limit
        )

    async def in_area(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        skip: int,
        limit: int,
    ) -> Sequence[Organization]:
        """Ищет организации внутри прямоугольной области.

        Args:
            lat1: Нижняя широта.
            lon1: Левая долгота.
            lat2: Верхняя широта.
            lon2: Правая долгота.
            skip: Смещение.
            limit: Лимит.

        Returns:
            Последовательность организаций.
        """
        low_lat, high_lat = sorted([lat1, lat2])
        low_lon, high_lon = sorted([lon1, lon2])
        return await organization_crud.by_area(
            self.session,
            lat1=low_lat,
            lon1=low_lon,
            lat2=high_lat,
            lon2=high_lon,
            skip=skip,
            limit=limit,
        )

    async def by_activity_tree(
        self, activity_id: int, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Ищет организации по всему поддереву деятельности.

        Args:
            activity_id: Корневой идентификатор.
            skip: Смещение.
            limit: Лимит.

        Returns:
            Последовательность организаций.
        """
        a_service = ActivityService(self.session)
        ids = await a_service.get_all_descendants_ids(activity_id)
        result: list[Organization] = []
        for aid in ids:
            chunk = await organization_crud.by_activity(
                self.session, activity_id=aid, skip=0, limit=limit + skip
            )
            result.extend(chunk)
        dedup: dict[int, Organization] = {o.id: o for o in result}
        ordered = sorted(dedup.values(), key=lambda x: x.id)
        return ordered[skip : skip + limit]

    async def in_radius(
        self, lat: float, lon: float, radius_m: float, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Ищет организации в радиусе, используя bounding box + точную фильтрацию по Хаверсину.

        Args:
            lat: Широта центра.
            lon: Долгота центра.
            radius_m: Радиус поиска в метрах.
            skip: Смещение.
            limit: Лимит.

        Returns:
            Список организаций внутри радиуса.
        """
        if radius_m <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Radius must be positive",
            )

        lat_min, lon_min, lat_max, lon_max = bounding_box_for_radius(
            lat, lon, radius_m
        )

        candidates = await organization_crud.by_area(
            self.session,
            lat1=lat_min,
            lon1=lon_min,
            lat2=lat_max,
            lon2=lon_max,
            skip=0,
            limit=10_000,
        )

        def _coords_from_org(o: Organization) -> tuple[float, float]:
            return float(o.building.latitude), float(o.building.longitude)

        filtered = filter_by_radius(
            candidates, _coords_from_org, lat, lon, radius_m
        )
        ordered = sorted(filtered, key=lambda x: x.id)
        return ordered[skip : skip + limit]
