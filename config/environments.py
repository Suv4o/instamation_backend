from dotenv import load_dotenv
import os

load_dotenv()

PYTHON_ENV = os.getenv("PYTHON_ENV")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
