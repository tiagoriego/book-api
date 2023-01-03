import os
from dotenv import load_dotenv

load_dotenv()

API_VERSION = os.getenv("API_VERSION")
API_TITLE = os.getenv("API_TITLE")
API_DESCRIPTION = os.getenv("API_DESCRIPTION")
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DB_CONNECTION = os.getenv("DB_CONNECTION")
