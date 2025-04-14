import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("USER_DATABASE_URI", "postgresql://postgres:123@localhost/db_flask")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("FLASK_JWT_SECRET_KEY")

