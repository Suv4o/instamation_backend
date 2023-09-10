import os

import schedule
import requests
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from pyppeteer import launch

from utils.decorators import requires_auth
from utils.enums import ErrorResponse
from routes.content import get_image_content
from routes.assets import get_random_image_form_db
from routes.settings import get_settings_from_db
from config.environments import TEMP_IMAGES_PATH
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

            schedule.every(3).minutes.do(post_image_to_instagram, current_user=self.current_user).tag(user_from_db.uid)

            return {"success": True, "message": "Scheduled!"}

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value

    @requires_auth
    def delete(self):
        try:
            user_from_db = get_user_from_db(self.current_user)
            current_job = schedule.get_jobs(user_from_db.uid)

            if not current_job:
                return {"success": False, "message": "No scheduled task!"}

            schedule.clear(user_from_db.uid)
            return {"success": True, "message": "Stopped!"}

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def post_image_to_instagram(current_user):
    image = get_random_image_form_db(current_user, "all")
    image_uuid = image.get("id")
    image_url = image.get("url")
    image_description = get_image_content(image_uuid)

    settings_from_db = get_settings_from_db(current_user)
    first_name = settings_from_db.get("instagram_username")
    password = settings_from_db.get("instagram_password")

    handle_image_upload(image_url, image_description, first_name, password)


def get_user_from_db(current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()

        if not user:
            raise NotFound("Image not found.")

        return user

    except Exception as e:
        return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def signal_handler(signum, frame):
    print("Received SIGINT signal")
    raise KeyboardInterrupt


def handle_image_upload(image_url, image_description, first_name, password):
    from utils.upload_instagram_image import upload_image

    upload_image(
        file_url=image_url,
        description=image_description,
        user_name=first_name,
        password=password,
        temp_image_path=TEMP_IMAGES_PATH,
    )
