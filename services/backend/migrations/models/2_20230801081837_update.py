from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Add the new column with NULL constraint
        ALTER TABLE results ADD COLUMN job_id VARCHAR(8);

        -- Update existing rows to provide a non-NULL random value
        UPDATE results SET job_id = substr(md5(random()::text), 1, 8) WHERE job_id IS NULL;

        -- Set the NOT NULL constraint after updating the existing rows
        ALTER TABLE results ALTER COLUMN job_id SET NOT NULL;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "results" DROP COLUMN "job_id";"""
