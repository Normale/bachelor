from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Header
from fastapi.responses import FileResponse, Response
from src.auth.jwthandler import get_current_user
from src.crud.results import create_result, delete_result
from src.schemas.token import Status
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
from fastapi import exceptions
from starlette.status import HTTP_304_NOT_MODIFIED
from src.config import settings
from pathlib import Path
from src.crud.images import upload_image_to_storage
from azure.storage.blob import BlobServiceClient
import io
from fastapi.responses import FileResponse, Response, JSONResponse, StreamingResponse

router = APIRouter(tags=["Results"])

class StatusMessage(BaseModel):
    message: str

from src.schemas.results import ResultInSchema


@router.post(
    "/results/{username}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def upload_result(
    username: str,
    result_data: ResultInSchema,
    current_user = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to upload results."
        )

    # Continue with the rest of your logic to create the result and return the URL
    result_url = await create_result(result_data)
    return StatusMessage(message=f"Result uploaded successfully. URL: {result_url}")


@router.get(
    "/results",
    dependencies=[Depends(get_current_user)]
)
async def get_results(
    current_user = Depends(get_current_user),
    if_modified_since: Optional[str] = Header(None)
):
    # Get the directory path for the user's results
    results_dir = Path(settings.RESULT_UPLOAD_DIR) / current_user.username
    # Create the directory if it does not exist
    results_dir.mkdir(parents=True, exist_ok=True)
    # Get a list of all the result file names in the directory
    result_names = [f.name for f in results_dir.glob("*.*")]
    # Convert the result file names to URLs
    result_urls = [
        f"{settings.BASE_RESULT_URL}/{current_user.username}/{name}"
        for name in result_names
    ]
    # Return the list of result URLs as JSON
    return result_urls



@router.get(
    "/results/{blob_name:path}",
)
async def get_image(
    blob_name: str,
):
    blob_path = f"results/{blob_name}"
    blob_service_client = BlobServiceClient.from_connection_string(settings.STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(settings.CONTAINER_NAME, blob_path)

    if not blob_client.exists():
        raise HTTPException(status_code=404, detail="Image not found.")
    else:
        blob_stream = blob_client.download_blob().content_as_bytes()
        return StreamingResponse(io.BytesIO(blob_stream), media_type="image/*")


@router.delete(
    "/results/{username}/{result_name}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def delete_result(
    username: str,
    result_name: str,
    current_user = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete results."
        )
    delete_result(f"./storage/results/{username}/{result_name}")
    return StatusMessage(message="Result deleted successfully.")

@router.patch(
    "/results/{username}/{result_name}",
    response_model=StatusMessage,
    dependencies=[Depends(get_current_user)]
)
async def update_result(
    username: str,
    result_name: str,
    result: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update results."
        )
    delete_result(f"./storage/results/{username}/{result_name}")
    result_url = await update_result(result, username)
    return StatusMessage(message="Result updated successfully.")


