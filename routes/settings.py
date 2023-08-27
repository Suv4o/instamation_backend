from cryptography.fernet import Fernet
from flask_restful import Resource, reqparse

from utils.decorators import requires_auth
from utils.helpers import encrypt_string, decrypt_string
from utils.enums import ErrorResponse
from config.database import db_session
from models import Settings, Users


class SettingsRoute(Resource):
    """Settings route definition"""

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
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value

    @requires_auth
    def get(self):
        try:
            return get_settings_from_db(self.current_user)

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def store_settings_in_db(args, current_user):
    user_name = args["instagram_username"]
    password = args["instagram_password"]
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        settings = Settings.query.join(Settings.user).filter(Users.uid == user.uid).first()

        if settings:
            encryption_key = settings.encryption_key

            settings.instagram_username = user_name
            settings.instagram_password = encrypt_string(password, encryption_key)
            db_session.commit()

        else:
            encryption_key = Fernet.generate_key()

            settings = Settings(
                user_id=user.uid,
                instagram_username=user_name,
                instagram_password=encrypt_string(password, encryption_key),
                encryption_key=encryption_key.decode("utf-8"),
            )
            db_session.add(settings)
            db_session.commit()

    except Exception as e:
        return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def get_settings_from_db(current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        settings = Settings.query.join(Settings.user).filter(Users.uid == user.uid).first()

        return {
            "instagram_username": settings.instagram_username if settings else "",
            "instagram_password": decrypt_string(settings.instagram_password, settings.encryption_key)
            if settings
            else "",
        }

    except Exception as e:
        return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value
