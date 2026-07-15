from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./shopping_list.db"
    supabase_url: str = ""
    supabase_key: str = ""
    cors_origins: str = "*"
    app_title: str = "ListTo API"
    app_version: str = "0.1.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
