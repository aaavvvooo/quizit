from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    app_name: str = "CHGK Platform API"
    environment: str = "dev"

    database_url: str
    alembic_url: str

    jwt_secret: str = "change_me"  # phase 0: placeholder


settings = Settings()
