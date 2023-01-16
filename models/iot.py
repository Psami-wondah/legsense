from pydantic import BaseModel
from datetime import datetime


class SensorData(BaseModel):
    T1: str
    T2: str
    T3: str
    F1: str
    F2: str
    F3: str
    M1: str
    M2: str
    H1: str
    H2: str

class SensorDataDb(SensorData):
    date_added: datetime
    short_id: str

class SensorState(BaseModel):
    active: bool