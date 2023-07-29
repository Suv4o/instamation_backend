from flask_restful import Resource
from utils import auth


class Auth(Resource):
    @auth
    def get(self):
        return {"success": True}
