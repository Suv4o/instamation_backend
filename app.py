from flask import Flask
from flask_restful import Resource, Api
from waitress import serve

from config import PYTHON_ENV, SERVER_HOST, SERVER_PORT

import logging

logging.basicConfig(level=logging.DEBUG)
console = logging.getLogger("app")

app = Flask("app")
debug = True if PYTHON_ENV == "development" else False

if __name__ == "__main__":
    console.info("Starting server...")
    serve(app, host=SERVER_HOST, port=SERVER_PORT)
