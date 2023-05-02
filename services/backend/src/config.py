from pydantic import BaseSettings


class Settings(BaseSettings):
    IMAGE_UPLOAD_DIR: str = "storage/images"
    STYLE_IMAGES_DIR: str = "storage/styles"
    BASE_IMAGE_URL: str = "http://localhost:5000/images"
    BASE_STYLE_IMAGES_URL: str = "http://localhost:5000/style"

settings = Settings()
