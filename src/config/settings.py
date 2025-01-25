from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    BASE_URL: str
    

    class Config:
        env_file = ".env"
