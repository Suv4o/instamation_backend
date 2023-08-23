from appwrite.input_file import InputFile
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from utils.decorators import requires_auth
from utils.helpers import Appwrite
from config.environments import APPWRITE_BUCKET_ID


class AssetsRoute(Resource):
    """Assets route definition"""

    @requires_auth
    def post(self):
        try:
            appwrite = Appwrite()
            result = appwrite.storage.create_file(APPWRITE_BUCKET_ID, "123", InputFile.from_path("./test.jpg"))

            return result

        except Exception as e:
            raise BadRequest(e)
