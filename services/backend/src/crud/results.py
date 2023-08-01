from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Results
from src.schemas.results import ResultInSchema, ResultOutSchema

async def create_result(result: ResultInSchema) -> ResultOutSchema:
    try:
        result_obj = await Results.create(**result.dict())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Result creation failed")

    return await ResultOutSchema.from_tortoise_orm(result_obj)

async def get_result(result_id: int) -> ResultOutSchema:
    try:
        result_obj = await Results.get(id=result_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Result {result_id} not found")

    return await ResultOutSchema.from_tortoise_orm(result_obj)

async def update_result(result_id: int, result: ResultInSchema) -> ResultOutSchema:
    await Results.filter(id=result_id).update(**result.dict(exclude_unset=True))
    result_obj = await Results.get(id=result_id)

    return await ResultOutSchema.from_tortoise_orm(result_obj)

async def delete_result(result_id: int) -> None:
    deleted_count = await Results.filter(id=result_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Result {result_id} not found")
