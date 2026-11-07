from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "netops"
    postgres_password: str = "change-me"
    postgres_db: str = "netops"
    postgres_host: str = "db"
    redis_url: str = "redis://redis:6379/0"
    mock_mode: bool = True
    netbox_url: str = "https://demo.netbox.dev"
    netbox_token: str = ""
    netbox_site: str = ""
    jwt_secret: str = "secret"
    jwt_expire_minutes: int = 480


    @property
    def database_url(self) -> str:
        return (f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:5432/{self.postgres_db}")


settings = Settings()