from flask import Flask
from flask_restful import Api
from routes import Auth, Settings
from config.server_restart_handler import run_server, generate_requirements


app = Flask("app")
app.config["BUNDLE_ERRORS"] = True
api = Api(app, prefix="/api")


# Routes
api.add_resource(Auth, "/")
api.add_resource(Settings, "/settings")

if __name__ == "__main__":
    generate_requirements()
    run_server(app)
