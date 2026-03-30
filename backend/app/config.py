from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    ENCRYPTION_KEY: str
    ENCRYPTION_SALT: str
    DATABASE_URL: str
    FRONTEND_URL: str
    ENVIRONMENT: str = "dev"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "prod"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()