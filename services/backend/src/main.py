import aiopg
import asyncio
import json

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM
from src.kafka.register import register_kafka
from src.kafka.config import KAFKA_CONFIG



# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

"""
import 'from src.routes import users, notes' must be after 'Tortoise.init_models'
why?
https://stackoverflow.com/questions/65531387/tortoise-orm-for-python-no-returns-relations-of-entities-pyndantic-fastapi
"""
from src.routes import users, notes, images, styles, results, notifications

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
# app.include_router(notes.router)
app.include_router(images.router)
app.include_router(styles.router)
app.include_router(results.router)
app.include_router(notifications.router)
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)
register_kafka(app, config=KAFKA_CONFIG)

@app.get("/")
def home():
    print("XD")
    return "Hello, World!"





@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive data from the client
        received_data = await websocket.receive_json()
        print("Received data from the client:", received_data)

        # Send the "processing" state with queue_length and estimated_time details
        processing_response = {
            "state": "processing",
            "details": {
                "queue_length": 123,
                "estimated_time": 123
            }
        }
        await websocket.send_json(processing_response)
        received_data_bytes = json.dumps(received_data).encode('utf-8')

        await app.state.producer.send_and_wait(received_data["selectedStyle"], received_data_bytes)# json.dumps(received_data).encode('utf-8'))


        
        result = await wait_for_row_update(received_data)
        if not result:
            # Handle the case where the row is not found, maybe send a failure response
            return

        # Send the "finished" state with the result URL
        finished_response = {
            "state": "finished",
            # "result": "http://localhost:5000/style/rpg/images/_with_soft_skinice_perfect_face_oth_0_e0dbc1bf-4f7b-4bab-bda3-fc61f5242984_12.jpg"
            "result": f"http://localhost:5000/results/{result['result_url']}"
        }
        await websocket.send_json(finished_response)



async def wait_for_row_update(received_data):
    # Maximum number of retries before giving up
    dsn = 'dbname=bachelor_db user=bachelor password=bachelor host=db port=5432'
    result = None
    max_retries = 3
    retry_count = 0
    async with aiopg.connect(dsn) as conn:
        async with conn.cursor() as cur:
            while result is None and retry_count < max_retries:
                retry_count += 1
                print("waiting for notification")
                await cur.execute("LISTEN results;")
                try:
                    msg = await asyncio.wait_for(conn.notifies.get(), timeout=10)
                except TimeoutError:
                    continue         
                payload_data = json.loads(msg.payload)  # Parse the payload as JSON
                print(f"Received notification: {payload_data}")
                # check if styleimage and image are equal
                print(payload_data.get("content_image") == received_data["selectedImage"])
                print(payload_data.get("style_image") == received_data["selectedStyleImage"])
                if (payload_data.get("content_image") == received_data["selectedImage"]
                    and payload_data.get("style_image") == received_data["selectedStyleImage"]):
                    result = payload_data
                    return result