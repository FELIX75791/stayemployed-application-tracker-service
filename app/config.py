import os
from dotenv import load_dotenv

load_dotenv()

SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
