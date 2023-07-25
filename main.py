from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv
from waitress import serve
import logging
import os

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
console = logging.getLogger("app")

PYTHON_ENV = os.getenv("PYTHON_ENV")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")

app = Flask("app")
debug = True if PYTHON_ENV == "development" else False

if __name__ == "__main__":
    console.info("Starting server...")
    serve(app, host=SERVER_HOST, port=SERVER_PORT)
