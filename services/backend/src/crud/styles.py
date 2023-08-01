from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Styles
from src.schemas.styles import StyleInSchema, StyleOutSchema


async def create_style(style: StyleInSchema) -> StyleOutSchema:
    try:
        style_obj = await Styles.create(**style.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Style creation failed")
    
    return await StyleOutSchema.from_tortoise_orm(style_obj)



async def get_style(style_id: int) -> StyleOutSchema:
    try:
        style_obj = await Styles.get(id=style_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Style {style_id} not found")

    return await StyleOutSchema.from_tortoise_orm(style_obj)


async def update_style(style_id: int, style: StyleInSchema) -> StyleOutSchema:
    await Styles.filter(id=style_id).update(**style.dict(exclude_unset=True))
    style_obj = await Styles.get(id=style_id)

    return await StyleOutSchema.from_tortoise_orm(style_obj)


async def delete_style(style_id: int) -> None:
    deleted_count = await Styles.filter(id=style_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Style {style_id} not found")
