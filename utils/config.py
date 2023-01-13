import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
SOCKET_PROTECT_TOKEN = os.getenv('SOCKET_PROTECT_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')