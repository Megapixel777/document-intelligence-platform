from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Document Intelligence Platform"
    app_version: str = "0.1.0"

    documents_path: str = "documents"

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()