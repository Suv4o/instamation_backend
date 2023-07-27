from flask import Flask
from flask_restful import Api
from routes.auth import Auth
from config import run_server


app = Flask("app")
app.debug = True
api = Api(app, prefix="/api")


# Routes
api.add_resource(Auth, "/")

if __name__ == "__main__":
    run_server(app)
