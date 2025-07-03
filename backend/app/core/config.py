from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_port: int = 8000
    embedding_model: str 
    gemini_api_key: str 
    gemini_model_name: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
