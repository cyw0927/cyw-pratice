from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cat Game Backend"
    app_env: str = "local"
    database_url: str = "sqlite+pysqlite:///./cat_game.db"
    grading_image: str = "cat-game-python-grader:3.12"

    # Exact limits are product/operations policy and remain TBD. Safe local MVP
    # defaults are configurable and must be approved before production rollout.
    grading_timeout_seconds: float = 5.0
    grading_memory: str = "128m"
    grading_cpus: float = 0.5
    grading_pids_limit: int = 64
    grading_output_bytes: int = 65536
    grading_max_concurrency: int = 2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
