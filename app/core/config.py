from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cat Game Backend - Part 2 MVP"
    database_url: str = "sqlite:///./cat_game.db"
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CAT_GAME_")


settings = Settings()
