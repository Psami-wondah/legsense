from fastapi import APIRouter, Request
from db.config import db
from models.iot import SensorData, SensorDataDb
from datetime import datetime
from utils import config
import socketio
from typing import Any, List
from utils import config
from utils.utils import generate_short_id
import pymongo
from fastapi.responses import JSONResponse
from fastapi import status


iot = APIRouter(
    tags=["Iot 💻"],
    prefix="/api/v1/iot"
)

mgr = socketio.AsyncRedisManager(config.REDIS_URL)
sio: Any = socketio.AsyncServer(async_mode="asgi", client_manager=mgr, cors_allowed_origins="*")


@iot.post('/sensor-data')
async def post_sensor_data(data: SensorData, request: Request, key: str):
    if not key:
        return JSONResponse({"message": "pass in key"}, status_code=status.HTTP_400_BAD_REQUEST)
    if key != config.SOCKET_PROTECT_TOKEN:
        return JSONResponse({"message": "Invalid key"}, status_code=status.HTTP_400_BAD_REQUEST)
    leg_data={
        "date_added": datetime.utcnow(),
        "short_id": generate_short_id(),
        **data.dict()
    }
    sio_data = {**leg_data, "date_added":str(leg_data["date_added"])}
    db.legdata.insert_one(leg_data)
    await sio.emit("new_sensor_data", sio_data)
    c = await request.json()
    return {"message": "New leg data added", "data": c}

@iot.get('/sensor-data', response_model=List[SensorDataDb])
async def get_sensor_data(key: str):
    if not key:
        return JSONResponse({"message": "pass in key"}, status_code=status.HTTP_400_BAD_REQUEST)
    if key != config.SOCKET_PROTECT_TOKEN:
        return JSONResponse({"message": "Invalid key"}, status_code=status.HTTP_400_BAD_REQUEST)
    db_leg_data = db.legdata.find().sort([("date_added", pymongo.DESCENDING)])
    leg_data = [SensorDataDb(**leg_datum) for leg_datum in db_leg_data]
    return leg_data


@sio.on("connect") 
async def connect(sid, env, auth):
    if auth:
        token = auth["token"]
        if token == config.SOCKET_PROTECT_TOKEN:
            print("SocketIO connect")
            await sio.emit("connect", f"{sid} connected")
        else:
            raise ConnectionRefusedError("Incorrect connect token")
    else:
        raise ConnectionRefusedError("no auth token")


@sio.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")