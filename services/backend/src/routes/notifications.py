from fastapi import APIRouter, Depends
from src.auth.jwthandler import get_current_user
import asyncio
import aiopg
import json


router = APIRouter(tags=["Notifications"])

@router.get("/listen-for-changes")
async def listen_for_changes(id: int):
    # Connection details - replace with your actual details
    dsn = 'dbname=bachelor_db user=bachelor password=bachelor host=db port=5432'

    async with aiopg.connect(dsn) as conn:
        async with conn.cursor() as cur:
            await cur.execute("LISTEN results;")
            msg = await asyncio.wait_for(conn.notifies.get(), timeout=10)
            # payload_data = json.loads(msg.payload)  # Parse the payload as JSON
            print(f"Received notification: {msg}")
    
    # Return a simple message. You might want to return something more meaningful in your application.
    return {"message": "Received notification"}
