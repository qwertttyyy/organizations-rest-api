from urllib.parse import quote_plus

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения.

    Атрибуты:
        DB_USER: имя пользователя БД.
        DB_PASS: пароль БД.
        DB_HOST: хост БД.
        DB_PORT: порт БД.
        DB_NAME: имя базы данных.
        DATABASE_URL: если задано используется как есть, иначе собирается из составляющих.
        API_KEY: API ключ для доступа к роутам.
        APP_NAME: название приложения.
        DEBUG: флаг debug.
    """

    DB_USER: str
    DB_PASS: SecretStr
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    DATABASE_URL: str | None = None

    API_KEY: str
    APP_NAME: str = "Organizations REST API"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra='allow'
    )

    def get_database_url(self) -> str:
        """Возвращает корректный DATABASE_URL.

        Если в окружении указан DATABASE_URL — возвращает его.
        Иначе собирает строку подключения и корректно экранирует пароль.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        pwd = quote_plus(self.DB_PASS.get_secret_value())
        return f"postgresql+asyncpg://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
