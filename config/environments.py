from dotenv import load_dotenv
import os

load_dotenv()

PYTHON_ENV = os.getenv("PYTHON_ENV")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
AUTH0_RS256_ALGORITHMS = os.getenv("AUTH0_RS256_ALGORITHMS")
