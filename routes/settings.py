from flask_restful import Resource, reqparse

from utils.decorators import requires_auth


class Settings(Resource):
    @requires_auth
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("instagram_username", type=str, required=True)
        parser.add_argument("instagram_password", type=str, required=True)
        args = parser.parse_args()
        return {"success": True, "current_user": self.current_user}
