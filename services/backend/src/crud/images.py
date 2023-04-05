import hashlib
from pathlib import Path
from fastapi import UploadFile
from src.config import settings
import aiofiles
import os
import hashlib
from pathlib import Path
from fastapi import UploadFile
from src.config import settings
import aiofiles


async def upload_image_to_storage(image: UploadFile, username: str) -> str:
    """
    Upload an image file to the server's file system.

    Parameters:
    - image: the image file to upload
    - username: the username of the user who uploaded the image

    Returns:
    - The URL of the uploaded image.
    """
    file_name = image.filename
    # replace filename with number of image in folder
    no_images = len(os.listdir(f"{settings.IMAGE_UPLOAD_DIR}/{username}"))
    file_name = f"{no_images}.{file_name.split('.')[-1]}"
    upload_dir = Path(settings.IMAGE_UPLOAD_DIR) / username
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file_name

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write
    # Return the URL of the uploaded image
    return f"{settings.BASE_IMAGE_URL}/{username}/{file_name}"



def delete_file(file_path: str):
    """
    Delete a file from the server's file system.

    Parameters:
    - file_path: the path of the file to delete
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
