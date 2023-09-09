from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "results" ADD "result_url" VARCHAR(4096) NOT NULL;
        ALTER TABLE "results" DROP COLUMN "job_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "results" ADD "job_id" VARCHAR(255) NOT NULL;
        ALTER TABLE "results" DROP COLUMN "result_url";"""
