# Organizations REST API

Асинхронный FastAPI REST API для справочника **Зданий**, **Организаций** и **Видов деятельности**.

## Быстрое описание

* Все эндпоинты защищены API-ключом: передавайте заголовок `X-API-Key: <API_KEY>`.
* Документация: `/docs` (Swagger) и `/redoc`.

## Эндпоинты (кратко)

* `GET /buildings` — список зданий (пагинация: `skip`, `limit`).
* `GET /organizations/{organization_id}` — детальная информация об организации.
* `GET /organizations/by-building/{building_id}` — организации в здании.
* `GET /organizations/by-activity/{activity_id}` — организации по виду деятельности.
* `GET /organizations/in-radius?lat=&lon=&radius=` — поиск по радиусу (метры).
* `GET /organizations/in-area?lat1=&lon1=&lat2=&lon2=` — поиск в прямоугольнике.
* `GET /organizations/search?name=` — поиск по названию (ILIKE).
* `GET /organizations/search/by-activity-tree/{activity_id}` — поиск по дереву деятельностей.

Все списочные эндпоинты поддерживают `skip` и `limit` (по умолчанию `skip=0`, `limit=100`).

## Конфигурация (`.env`)

Пример необходимых переменных в .env.example:

```
# Database settings
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=5432
DB_NAME=

# Docker settings
APP_PORT=
DB_CONTAINER_PORT=

# Другие настройки
API_KEY=
APP_NAME=
DEBUG=

```

## Запуск через Docker

1. Создать `.env`
2. Сборка и запуск контейнеров:

```bash
docker compose up --build -d
```

3. После старта контейнеров **отдельно** наполнить БД:

```bash
docker compose exec web python scripts/seed.py
```

4. Проверить API: `http://localhost:8000/docs` (Swagger).

