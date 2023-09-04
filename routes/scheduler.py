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
            all_jobs = schedule.get_jobs()
            print(all_jobs)
            schedule.every(1).seconds.do(test_print).tag(user_from_db.uid)

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


def test_print():
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
