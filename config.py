from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PORT: str  # Temporary
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_EXPIRE_MINUTES: str
    SENDPULSE_API_ID: str
    SENDPULSE_API_SECRET: str
    SEND_EMAIL: bool
    KINOPOISK_TOKEN: str

    class Config:
        env_file = "./.env"


settings = Settings()
