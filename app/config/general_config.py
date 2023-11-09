from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = os.getenv("JWT_ALGO")

APP_PREFIX = os.getenv("APP_PREFIX")
