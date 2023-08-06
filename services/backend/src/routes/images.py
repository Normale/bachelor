# routes/images.py

from urllib.parse import urljoin
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from fastapi.responses import FileResponse, Response, JSONResponse, StreamingResponse
from src.auth.jwthandler import get_current_user
from src.crud.images import upload_image_to_storage, delete_file_from_storage
from src.schemas.token import Status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import exceptions
from src.config import settings
from pathlib import Path
from azure.storage.blob import BlobServiceClient
import io


router = APIRouter(tags=["Images"])

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
    response = await upload_image_to_storage(image, current_user.username)
    return response


@router.get(
    "/images",
    dependencies=[Depends(get_current_user)]
)
async def get_images(current_user = Depends(get_current_user)):
    blob_service_client = BlobServiceClient.from_connection_string(settings.STORAGE_CONNECTION_STRING)
    blob_list = blob_service_client.get_container_client(settings.CONTAINER_NAME).list_blobs(current_user.username)

    # Now we use the BASE_IMAGE_URL from your settings
    base_url = settings.BASE_IMAGE_URL
    image_urls = [urljoin(base_url, blob.name) for blob in blob_list]

    return image_urls

@router.get(
    "/images/{blob_name:path}",
    dependencies=[Depends(get_current_user)]
)
async def get_image(
    blob_name: str,
    current_user = Depends(get_current_user),
):
    blob_service_client = BlobServiceClient.from_connection_string(settings.STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(settings.CONTAINER_NAME, blob_name)

    if not blob_client.exists():
        raise HTTPException(status_code=404, detail="Image not found.")
    else:
        blob_stream = blob_client.download_blob().content_as_bytes()
        return StreamingResponse(io.BytesIO(blob_stream), media_type="image/*")


@router.delete(
    "/images/{blob_name:path}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def delete_image(
    blob_name: str,
    current_user = Depends(get_current_user)
):
    await delete_file_from_storage(blob_name)
    return StatusMessage(message="Image deleted successfully.")

@router.patch(
    "/images/{blob_name:path}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def update_image(
    blob_name: str,
    image: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    await delete_file_from_storage(blob_name)
    await upload_image_to_storage(image, blob_name)
    return StatusMessage(message="Image updated successfully.")
