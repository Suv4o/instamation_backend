from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from utils.decorators import requires_auth
from config.database import db_session
from models import Settings, Users


class SettingsRoute(Resource):
    @requires_auth
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("instagram_username", type=str, required=True)
            parser.add_argument("instagram_password", type=str, required=True)
            args = parser.parse_args()
            store_settings_in_db(args, current_user=self.current_user)

            return {"success": True, "message": "Settings saved successfully!"}
        except Exception as e:
            raise BadRequest(e)


def store_settings_in_db(args, current_user):
    user_name = args["instagram_username"]
    password = args["instagram_password"]
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        settings = Settings.query.join(Settings.user).filter(Users.uid == user.uid).first()

        if settings:
            settings.instagram_username = user_name
            settings.instagram_password = password
            db_session.commit()
        else:
            settings = Settings(user_id=user.uid, instagram_username=user_name, instagram_password=password)
            db_session.add(settings)
            db_session.commit()
    except Exception as e:
        raise BadRequest(e)
