import io, os, uuid

from PIL import Image
from appwrite.input_file import InputFile
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage

from utils.decorators import requires_auth
from utils.helpers import Appwrite
from config.environments import APPWRITE_BUCKET_ID, TEMP_IMAGES_PATH


class AssetsRoute(Resource):
    """Assets route definition"""

    @requires_auth
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=FileStorage, location="files")
            args = parser.parse_args()
            image_file = args["image"]
            image_extension = (
                "jpg"
                if image_file.filename.split(".")[-1] in ["jpeg", "jpg"]
                else "png"
                if image_file.filename.split(".")[-1] in ["png"]
                else None
            )

            if not image_extension:
                raise BadRequest("Invalid image file")

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
            os.remove(f"{TEMP_IMAGES_PATH}/{image_uuid}.{image_extension}")

            return {"success": True, "message": "File uploaded successfully"}
        except Exception as e:
            raise BadRequest(e)


def file_storage_to_binary(file: FileStorage) -> bytes:
    return file.read()
