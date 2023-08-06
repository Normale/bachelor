from pydantic import BaseSettings
from src.secret import AZURE_CONNECTION_STRING

class Settings(BaseSettings):
    IMAGE_UPLOAD_DIR: str = "storage/images/"
    RESULT_UPLOAD_DIR: str = "storage/images/"
    STYLE_IMAGES_DIR: str = "storage/styles"
    BASE_IMAGE_URL: str = "http://localhost:5000/images/"
    BASE_STYLE_IMAGES_URL: str = "http://localhost:5000/style"
    BASE_RESULT_URL: str = "http://localhost:5000/style"
    STORAGE_CONNECTION_STRING: str = AZURE_CONNECTION_STRING
    CONTAINER_NAME: str = "bachelor"
settings = Settings()
