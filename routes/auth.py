from flask_restful import Resource
from utils.decorators import requires_auth


class Auth(Resource):
    @requires_auth
    def get(self):
        return {"success": True, "current_user": self.current_user}
