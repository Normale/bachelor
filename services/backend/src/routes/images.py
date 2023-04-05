from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Header
from fastapi.responses import FileResponse, Response
from src.auth.jwthandler import get_current_user
from src.crud.images import upload_image_to_storage, delete_file
from src.schemas.token import Status
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
from fastapi import exceptions
from starlette.status import HTTP_304_NOT_MODIFIED
from src.config import settings
from pathlib import Path
def parse_date(date_string: str) -> datetime:
    try:
        return datetime.fromisoformat(date_string)
    except ValueError:
        # Handle invalid input
        raise ValueError("Invalid date format. Must be ISO 8601 format: YYYY-MM-DDTHH:MM:SS.ssssss")


router = APIRouter()

class StatusMessage(BaseModel):
    message: str


@router.post(
    "/images",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def upload_image(
    image: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    image_url = await upload_image_to_storage(image, current_user.username)
    return StatusMessage(message=f"Image uploaded successfully. URL: {image_url}")

@router.get(
    "/images",
    dependencies=[Depends(get_current_user)]
)
async def get_images(
    current_user = Depends(get_current_user),
    if_modified_since: Optional[str] = Header(None)
):
    # Get the directory path for the user's images
    images_dir = Path(settings.IMAGE_UPLOAD_DIR) / current_user.username
    # Create the directory if it does not exist
    images_dir.mkdir(parents=True, exist_ok=True)
    # Get a list of all the image file names in the directory
    image_names = [f.name for f in images_dir.glob("*.*")]
    # Convert the image file names to URLs
    image_urls = [
        f"{settings.BASE_IMAGE_URL}/{current_user.username}/{name}"
        for name in image_names
    ]
    # Return the list of image URLs as JSON
    return image_urls

    

@router.get(
    "/images/{username}/{image_name}",
    dependencies=[Depends(get_current_user)]
)
async def get_image(
    username: str,
    image_name: str,
    current_user = Depends(get_current_user),
):
    if current_user.username != username:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this image."
        )
        
    file_path = f"./storage/images/{current_user.username}/{image_name}"
    return FileResponse(file_path)


@router.delete(
    "/images/{username}/{image_name}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def delete_image(
    username: str,
    image_name: str,
    current_user = Depends(get_current_user)
):
    if current_user.username != username:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this image."
        )
    delete_file(f"./storage/images/{current_user.username}/{image_name}")
    return StatusMessage(message="Image deleted successfully.")


@router.patch(
    "/images/{username}/{image_name}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def update_image(
    username: str,
    image_name: str,
    image: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    delete_file(f"./storage/images/{current_user.username}/{image_name}")
    image_url = await upload_image_to_storage(image, current_user.username)
    return StatusMessage(message="Image updated successfully.")
