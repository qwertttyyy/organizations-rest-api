from math import radians, sin, cos, asin, sqrt, degrees
from typing import Tuple, Iterable, List


def haversine_distance_m(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Вычисляет расстояние в метрах между двумя точками по формуле Хаверсина.

    Args:
        lat1: Широта первой точки в градусах.
        lon1: Долгота первой точки в градусах.
        lat2: Широта второй точки в градусах.
        lon2: Долгота второй точки в градусах.

    Returns:
        Расстояние между точками в метрах.
    """
    r = 6371000.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))
    return r * c


def bounding_box_for_radius(
    lat: float, lon: float, radius_m: float
) -> Tuple[float, float, float, float]:
    """Возвращает приближённую bounding box (lat_min, lon_min, lat_max, lon_max) для заданного круга.

    Приближение основано на экваториальном радиусе и учитывает изменение широты/долготы.
    Для малых радиусов (несколько десятков километров) погрешность невелика.

    Args:
        lat: Широта центра в градусах.
        lon: Долгота центра в градусах.
        radius_m: Радиус в метрах.

    Returns:
        Кортеж (lat_min, lon_min, lat_max, lon_max).
    """
    earth_radius = 6371000.0
    lat_delta = degrees(radius_m / earth_radius)
    lon_delta = degrees(
        radius_m / (earth_radius * cos(radians(lat)) if abs(lat) < 90 else 1.0)
    )
    lat_min = lat - lat_delta
    lat_max = lat + lat_delta
    lon_min = lon - lon_delta
    lon_max = lon + lon_delta
    return lat_min, lon_min, lat_max, lon_max


def point_in_rectangle(
    lat: float, lon: float, lat1: float, lon1: float, lat2: float, lon2: float
) -> bool:
    """Проверяет, лежит ли точка внутри прямоугольника (включительно).

    Поддерживает произвольный порядок координат прямоугольника (необязательно левый-низ / правый-верх).

    Args:
        lat: Широта проверяемой точки.
        lon: Долгота проверяемой точки.
        lat1: Широта первого угла прямоугольника.
        lon1: Долгота первого угла прямоугольника.
        lat2: Широта второго угла прямоугольника.
        lon2: Долгота второго угла прямоугольника.

    Returns:
        True, если точка внутри прямоугольника, иначе False.
    """
    low_lat, high_lat = (lat1, lat2) if lat1 <= lat2 else (lat2, lat1)
    low_lon, high_lon = (lon1, lon2) if lon1 <= lon2 else (lon2, lon1)
    return (low_lat <= lat <= high_lat) and (low_lon <= lon <= high_lon)


def filter_by_radius(
    items: Iterable[object],
    extract_latlon: callable,
    center_lat: float,
    center_lon: float,
    radius_m: float,
) -> List[object]:
    """Фильтрует коллекцию объектов, оставляя только те, чьи координаты лежат в радиусе.

    Args:
        items: Итерация объектов (например, организации).
        extract_latlon: Функция object -> (lat: float, lon: float).
        center_lat: Широта центра.
        center_lon: Долгота центра.
        radius_m: Радиус в метрах.

    Returns:
        Список объектов внутри радиуса.
    """
    result: List[object] = []
    for it in items:
        lat, lon = extract_latlon(it)
        if (
            haversine_distance_m(
                center_lat, center_lon, float(lat), float(lon)
            )
            <= radius_m
        ):
            result.append(it)
    return result
