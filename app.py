from flask import Flask, Blueprint
from flask_restful import Resource, Api
from waitress import serve
from config import SERVER_HOST, SERVER_PORT, Logger


app = Flask("app")
api = Api(app, prefix="/api")
console = Logger("app").get()


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
    console.info("Starting server...")
    serve(app, host=SERVER_HOST, port=SERVER_PORT)
