from tortoise.contrib.pydantic import pydantic_model_creator
from src.database.models import Results

ResultInSchema = pydantic_model_creator(
    Results, name="ResultIn", exclude_readonly=True
)
ResultOutSchema = pydantic_model_creator(
    Results, name="ResultOut", exclude=["created_at", "modified_at", "user"]
)
ResultDatabaseSchema = pydantic_model_creator(
    Results, name="Result", exclude=["created_at", "modified_at"]
)
