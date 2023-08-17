from flask import Flask
from flask_restful import Api
from routes import Auth
from config.server_restart_handler import run_server, generate_requirements


app = Flask("app")
api = Api(app, prefix="/api")


# Routes
api.add_resource(Auth, "/")

if __name__ == "__main__":
    generate_requirements()
    run_server(app)
