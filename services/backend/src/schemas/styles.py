from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users


StyleInSchema = pydantic_model_creator(
    Users, name="StyleIn", exclude_readonly=True
)
StyleOutSchema = pydantic_model_creator(
    Users, name="StyleOut", exclude=["created_at", "modified_at"]
)
StyleDatabaseSchema = pydantic_model_creator(
    Users, name="Style", exclude=["created_at", "modified_at"]
)
