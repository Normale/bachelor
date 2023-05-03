import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM


# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

"""
import 'from src.routes import users, notes' must be after 'Tortoise.init_models'
why?
https://stackoverflow.com/questions/65531387/tortoise-orm-for-python-no-returns-relations-of-entities-pyndantic-fastapi
"""
from src.routes import users, notes, images, styles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(notes.router)
app.include_router(images.router)
app.include_router(styles.router)
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.get("/")
def home():
    print("XD")
    return "Hello, World!"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Receive data from the client
    received_data = await websocket.receive_json()
    print("Received data from the client:", received_data)

    # Simulate processing
    await asyncio.sleep(1)  # Wait for 1 second to simulate processing time

    # Send the "processing" state with queue_length and estimated_time details
    processing_response = {
        "state": "processing",
        "details": {
            "queue_length": 123,
            "estimated_time": 123
        }
    }
    await websocket.send_json(processing_response)

    # Simulate waiting for processing to finish
    await asyncio.sleep(5)  # Wait for 5 seconds to simulate processing time

    # Send the "finished" state with the result URL
    finished_response = {
        "state": "finished",
        "result": "http://localhost:5000/style/rpg/images/_with_soft_skinice_perfect_face_oth_0_e0dbc1bf-4f7b-4bab-bda3-fc61f5242984_12.jpg"
    }
    await websocket.send_json(finished_response)