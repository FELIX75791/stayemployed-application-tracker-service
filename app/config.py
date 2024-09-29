import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Owen20020303!@localhost/test_db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeyfortesting1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
