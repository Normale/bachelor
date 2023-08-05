from fastapi import APIRouter, Depends
from src.auth.jwthandler import get_current_user
import asyncio
import aiopg

router = APIRouter(tags=["Notifications"])

@router.get("/listen-for-changes")
async def listen_for_changes():
    # Connection details - replace with your actual details
    dsn = 'dbname=bachelor_db user=bachelor password=bachelor host=db port=5432'

    async with aiopg.connect(dsn) as conn:
        async with conn.cursor() as cur:
            await cur.execute("LISTEN results;")
            msg = await asyncio.wait_for(conn.notifies.get(), timeout=10)
            print(f"Received notification: {msg.payload}")
    
    # Return a simple message. You might want to return something more meaningful in your application.
    return {"message": "Received notification"}
