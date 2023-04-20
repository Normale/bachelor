from typing import List

from fastapi import APIRouter, Depends, HTTPException
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


router = APIRouter(tags=["Styles"])


@router.get(
    "/styles",
    response_model=List[StyleOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_styles():
    return await StyleOutSchema.from_queryset(Styles.all())


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
