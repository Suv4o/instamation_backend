import io, os, uuid, random

from PIL import Image
from appwrite.input_file import InputFile
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

from utils.decorators import requires_auth
from utils.enums import ErrorResponse
from config.appwrite import Appwrite
from config.environments import APPWRITE_BUCKET_ID, APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, TEMP_IMAGES_PATH
from config.database import db_session
from models import Assets, Users


class AssetsRoute(Resource):
    """Assets route definition"""

    @requires_auth
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=FileStorage, location="files")
            args = parser.parse_args()
            image_file = args["image"]
            original_file_name = image_file.filename
            image_extension = (
                "jpg"
                if image_file.filename.split(".")[-1] in ["jpeg", "jpg"]
                else "png"
                if image_file.filename.split(".")[-1] in ["png"]
                else None
            )

            if not image_extension:
                return {"success": False, "message": "Invalid image file"}, ErrorResponse.BAD_REQUEST.value

            image_binary_data = file_storage_to_binary(image_file)
            image_uuid = uuid.uuid4()

            image = Image.open(io.BytesIO(image_binary_data))
            image.save(f"{TEMP_IMAGES_PATH}/{image_uuid}.{image_extension}")
            appwrite = Appwrite()
            appwrite.storage.create_file(
                APPWRITE_BUCKET_ID,
                image_uuid,
                InputFile.from_path(f"{TEMP_IMAGES_PATH}/{image_uuid}.{image_extension}"),
            )
            image_url = f"{APPWRITE_ENDPOINT}/storage/buckets/{APPWRITE_BUCKET_ID}/files/{image_uuid}/view?project={APPWRITE_PROJECT_ID}"
            clear_temp_images()

            image_details = {
                "original_file_name": original_file_name,
                "image_uuid": image_uuid,
                "image_url": image_url,
            }
            store_image_in_db(image_details, current_user=self.current_user)

            return {
                "success": True,
                "image": {"id": str(image_uuid), "url": image_url, "original_filename": original_file_name},
            }
        except Exception as e:
            clear_temp_images()
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value

    @requires_auth
    def get(self):
        try:
            return get_images_from_db(self.current_user)

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value

    @requires_auth
    def delete(self, image_uuid):
        try:
            delete_image_from_db(image_uuid, self.current_user)
            return {"success": True, "message": "Image deleted successfully!"}
        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


class AssetsRandomRoute(Resource):
    """Assets Random route definition"""

    @requires_auth
    def get(self):
        try:
            image_url = get_random_image_form_db(self.current_user)
            return image_url
        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


def file_storage_to_binary(file: FileStorage) -> bytes:
    return file.read()


def clear_temp_images():
    for file in os.listdir(TEMP_IMAGES_PATH):
        os.remove(f"{TEMP_IMAGES_PATH}/{file}")


def store_image_in_db(image_details, current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()

        image = Assets(
            aid=image_details["image_uuid"],
            url=image_details["image_url"],
            original_filename=image_details["original_file_name"],
            user_id=user.uid,
        )
        db_session.add(image)
        db_session.commit()

    except Exception as e:
        raise BadRequest(e)


def get_images_from_db(current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        assets = Assets.query.join(Assets.user).filter(Users.uid == user.uid).all()

        images = []

        for asset in assets:
            image = {
                "id": asset.aid,
                "url": asset.url,
                "original_filename": asset.original_filename,
            }
            images.append(image)

        if not assets:
            return {"success": True, "images": []}
        else:
            return {"success": True, "images": images}

    except Exception as e:
        raise BadRequest(e)


def delete_image_from_db(image_uuid, current_user):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        asset = Assets.query.filter(Assets.aid == image_uuid).first()

        if not asset:
            raise BadRequest("Image not found.")

        if asset.user_id != user.uid:
            raise Unauthorized("You are not authorized to delete this image.")

        appwrite = Appwrite()
        appwrite.storage.delete_file(
            APPWRITE_BUCKET_ID,
            image_uuid,
        )

        db_session.delete(asset)
        db_session.commit()
    except Exception as e:
        raise BadRequest(e)


def get_random_image_form_db(current_user, arg="url"):
    user_email = current_user["email"]
    try:
        user = Users.query.filter(Users.email == user_email).first()
        assets = Assets.query.join(Assets.user).filter(Users.uid == user.uid).all()

        random_image = random.choice(assets)

        random_image = {
            "id": random_image.aid,
            "url": random_image.url,
            "original_filename": random_image.original_filename,
            "created_at": random_image.created_at,
            "updated_at": random_image.updated_at,
        }

        if not random_image:
            raise NotFound("Image not found.")
        else:
            if arg == "all":
                return random_image
            else:
                return random_image.get(arg)

    except Exception as e:
        raise BadRequest(e)
