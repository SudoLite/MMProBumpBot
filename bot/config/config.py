from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    BASE_FARM_TIME: int = 21600
    BASE_MOON_BOUNS: int = 1000000
    TAPS_COUNT: list[int] = [45000, 99000]
    SLEEP_BETWEEN_CLAIM: list[int] = [3600, 5000]

    AUTO_BUY_BOOST: bool = True
    AUTO_CLAIM_TASKS: bool = True
    AUTO_CLAIM_MOON_BOUNS: bool = True

    DEFAULT_BOOST: str = "x3"

    BOOST_LEVLES: dict = {
        "x2": 4000000,
        "x3": 30000000,
        "x5": 200000000
    }

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()
