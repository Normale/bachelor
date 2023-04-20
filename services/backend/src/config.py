from pydantic import BaseSettings


class Settings(BaseSettings):
    IMAGE_UPLOAD_DIR: str = "storage/images"
    BASE_IMAGE_URL: str = "http://localhost:5000/images"


settings = Settings()
