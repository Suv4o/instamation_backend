from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from config import SERVER_HOST, SERVER_PORT, Logger


app = Flask("app")
console = Logger("app").get()

if __name__ == "__main__":
    console.info("Starting server...")
    serve(app, host=SERVER_HOST, port=SERVER_PORT)
