from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from routes import Auth, SettingsRoute, AssetsRoute, AssetsRandomRoute, ContentRoute
from config.server_restart_handler import run_server, generate_requirements


app = Flask("app")
CORS(app)
app.config["BUNDLE_ERRORS"] = True
api = Api(app, prefix="/api")


# Routes
api.add_resource(Auth, "/")
api.add_resource(SettingsRoute, "/settings")
api.add_resource(AssetsRoute, "/assets")
api.add_resource(AssetsRoute, "/assets/<image_uuid>", endpoint="assets_route")
api.add_resource(AssetsRandomRoute, "/assets/random", endpoint="assets_random_route")
api.add_resource(ContentRoute, "/content")
api.add_resource(ContentRoute, "/content/<image_uuid>", endpoint="content_route")

if __name__ == "__main__":
    generate_requirements()
    run_server(app)
