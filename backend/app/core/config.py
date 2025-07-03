from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_port: int = 8000
    embedding_model: str = "all-MiniLM-L6-v2"
    gemini_api_key: str = "AIzaSyA-UMkHFbBQhuoBuZUwhPZ_ayqaQp_kWsY"
    gemini_model_name: str ="gemini-2.0-flash"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
