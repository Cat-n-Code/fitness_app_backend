from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_url: str
    cors_allowed_origins: list[str]
    auth_token_lifetime: int = 3600
    auth_token_secret_key: str
    store_photos_path: str

    default_steps_goal: int = 8000
