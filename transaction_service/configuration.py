import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("USER_DATABASE_URI", "postgresql://postgres:123@localhost/transaction_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_SERVICE_URL = "http://localhost:5001"

    JWT_SECRET_KEY = os.getenv("FLASK_JWT_SECRET_KEY")

