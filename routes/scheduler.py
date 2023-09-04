import schedule
import time
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from utils.decorators import requires_auth
from utils.enums import ErrorResponse
from utils.helpers import run_scheduler
from models import Users


class SchedulerRoute(Resource):
    """Scheduler route definition"""

    @requires_auth
    def get(self):
        try:
            user_from_db = get_user_from_db(self.current_user)
            current_job = schedule.get_jobs(user_from_db.uid)

            if current_job:
                return {"success": True, "message": "Scheduled task already exist!"}

            schedule.every(3).minutes.do(post_image_to_instagram).tag(user_from_db.uid)

            return {"success": True, "message": "Scheduled!"}

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value

    @requires_auth
    def delete(self):
        try:
            user_from_db = get_user_from_db(self.current_user)
            schedule.clear(user_from_db.uid)

            return {"success": True, "message": "Stopped!"}

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def post_image_to_instagram():
    print("test print")


def get_user_from_db(current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()

        if not user:
            raise NotFound("Image not found.")

        return user

    except Exception as e:
        return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value
