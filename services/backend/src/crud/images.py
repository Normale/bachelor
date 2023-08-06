from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceNotFoundError
from fastapi import UploadFile, HTTPException
from src.config import settings
from typing import Union
from fastapi.responses import JSONResponse
import uuid

blob_service_client = BlobServiceClient.from_connection_string(settings.STORAGE_CONNECTION_STRING)


async def upload_image_to_storage(image: UploadFile, username: str) -> Union[JSONResponse, HTTPException]:
    """
    Upload an image file to Azure Blob Storage.

    Parameters:
    - image: the image file to upload
    - username: the username of the user who uploaded the image

    Returns:
    - A JSON response indicating success if the upload was successful, or an HTTPException indicating the error.
    """
    try:
        # Create a unique filename for the image
        blob_name = f"{username}/{str(uuid.uuid4())}.{image.filename.split('.')[-1]}"
        blob_client = blob_service_client.get_blob_client(settings.CONTAINER_NAME, blob_name)

        # Upload the image to Azure Blob Storage
        blob_client.upload_blob(await image.read(), overwrite=True)

        # Return a JSON response indicating success
        return JSONResponse(
            status_code=201, content={"message": "File uploaded successfully"}
        )
    except Exception as e:
        # Return a Status object indicating the error
        raise HTTPException(
            status_code=400, detail={"success": False, "message": str(e)}
        )


def delete_file_from_storage(blob_name: str) -> Union[JSONResponse, HTTPException]:
    """
    Delete a blob from Azure Blob Storage.

    Parameters:
    - blob_name: the name of the blob to delete

    Returns:
    - A JSON response with status code 200 if successful, or an HTTPException indicating the error.
    """
    try:
        blob_client = blob_service_client.get_blob_client(settings.CONTAINER_NAME, blob_name)
        blob_client.delete_blob()

        # Return a JSON response indicating success
        return JSONResponse(
            status_code=200, content={"message": "File deleted successfully"}
        )
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=404, detail={"success": False, "message": "Blob not found"}
        )
    except Exception as e:
        # Return a Status object indicating the error
        return HTTPException(
            status_code=400, detail={"success": False, "message": str(e)}
        )
