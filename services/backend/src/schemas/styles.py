from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Styles


StyleInSchema = pydantic_model_creator(
    Styles, name="StyleIn", exclude_readonly=True
)
StyleOutSchema = pydantic_model_creator(
    Styles, name="StyleOut", exclude=["created_at", "modified_at", "author"]
)
StyleDatabaseSchema = pydantic_model_creator(
    Styles, name="Style", exclude=["created_at", "modified_at"]
)
