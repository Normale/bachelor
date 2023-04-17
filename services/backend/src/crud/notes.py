import os
import uuid
from typing import Union
from fastapi import UploadFile, HTTPException
from src.config import settings
from pathlib import Path
from fastapi.responses import JSONResponse
from src.schemas.token import Status
from fastapi.responses import Response

async def upload_image_to_storage(
    image: UploadFile, username: str
) -> Union[Status, JSONResponse]:
    """
    Upload an image file to the server's file system.

    Parameters:
    - image: the image file to upload
    - username: the username of the user who uploaded the image

    Returns:
    - A JSON response indicating success if the upload was successful, or a Status object indicating the error.
    """
    try:
        # Create a unique filename for the image
        file_name = f"{str(uuid.uuid4())}.{image.filename.split('.')[-1]}"
        # Create the directory for the user's images if it does not exist
        upload_dir = Path(settings.IMAGE_UPLOAD_DIR) / username
        upload_dir.mkdir(parents=True, exist_ok=True)
        # Save the image to the server's file system
        file_path = upload_dir / file_name
        with file_path.open("wb") as buffer:
            buffer.write(await image.read())
        # Return a JSON response indicating success
        return JSONResponse(
            status_code=201, content={"message": "File uploaded successfully"}
        )
    except Exception as e:
        # Return a Status object indicating the error
        raise HTTPException(
            status_code=400, detail=Status(success=False, message=str(e))
        )


def delete_file(file_path: str) -> Union[Status, Response]:
    """
    Delete a file from the server's file system.

    Parameters:
    - file_path: the path of the file to delete

    Returns:
    - A JSON response with status code 200 if successful, or a Status object indicating the error.
    """
    try:
        os.remove(file_path)
        # Return a JSON response indicating success
        return Response(
            status_code=200, content={"message": "File deleted successfully"}
        )
    except Exception as e:
        # Return a Status object indicating the error
        return Status(success=False, message=f"123 {str(e)}")
