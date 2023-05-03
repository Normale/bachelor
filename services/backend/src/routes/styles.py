from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist
from src.database.models import Styles

from src.auth.jwthandler import get_current_user
from src.crud.styles import (
    create_style,
    delete_style,
    get_style,
    update_style,
)
from src.schemas.styles import (
    StyleInSchema,
    StyleOutSchema,
    StyleDatabaseSchema,
)
from src.schemas.token import Status
from src.config import settings

router = APIRouter(tags=["Styles"])


@router.get(
    "/styles",
    response_model=List[StyleOutSchema]
)
async def get_styles() -> List[StyleOutSchema]:
    # return dummy values for now
    return [
        StyleOutSchema(
            id=1,
            name="rpg",
            author_id=1,
        ),
        StyleOutSchema(
            id=2,
            name="fantasy",
            author_id=1,
        ),
    ]
    # return await StyleOutSchema.from_queryset(Styles.all())


@router.get(
    "/style/{style_id}",
    response_model=StyleOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_style(style_id: int) -> StyleOutSchema:
    try:
        style_obj = await get_style(style_id)
        return await StyleOutSchema.from_tortoise_orm(style_obj)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Style does not exist",
        )


@router.post(
    "/styles",
    response_model=StyleOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def create_style_endpoint(
    style: StyleInSchema,
) -> StyleOutSchema:
    style_obj = await create_style(style)
    return await StyleOutSchema.from_tortoise_orm(style_obj)


@router.patch(
    "/style/{style_id}",
    response_model=StyleOutSchema,
    dependencies=[Depends(get_current_user)],
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_style_endpoint(
    style_id: int,
    style: StyleInSchema,
) -> StyleOutSchema:
    style_obj = await update_style(style_id, style)
    return await StyleOutSchema.from_tortoise_orm(style_obj)


@router.delete(
    "/style/{style_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_style_endpoint(style_id: int) -> Status:
    await delete_style(style_id)
    return Status(message=f"Deleted style {style_id}")


@router.get(
    "/style/{style_name}/images",
)
async def get_style_images(
    style_name: str,
    if_modified_since: Optional[str] = Header(None)
) -> List[str]:
    # Get the directory path for the user's images
    images_dir = Path(settings.STYLE_IMAGES_DIR) / style_name / "images"
    # if images_dir doesn't exist, return 404
    if not images_dir.exists():
        raise HTTPException(
            status_code=404,
            detail="Style does not exist",
        )

    # Get a list of all the image file names in the directory
    image_names = [f.name for f in images_dir.iterdir() if f.is_file()]
    # Convert the image file names to URLs
    image_urls = [
        f"{settings.BASE_STYLE_IMAGES_URL}/{style_name}/images/{name}"
        for name in image_names
    ]
    # Return the list of image URLs as JSON
    return image_urls


@router.get(
    "/style/{style_name}/images/{image_name}",
)
async def get_image(
    style_name: str,
    image_name: str,
) -> FileResponse:  
    file_path = Path(settings.STYLE_IMAGES_DIR) / style_name / "images" / image_name
    # file_path = f"./storage/images/{style_name}/{image_name}"
    return FileResponse(file_path)

