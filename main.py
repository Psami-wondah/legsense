from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.iot import iot, sio
import socketio

app = FastAPI(
    title="LegSense",
    description="LegSense Apis",
    version="1.0.0",
)


app.include_router(iot)
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
