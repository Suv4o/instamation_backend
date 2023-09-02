from flask_restful import Resource
from transformers import pipeline

from utils.decorators import requires_auth
from utils.enums import ErrorResponse, ImageToTextModels


class ContentRoute(Resource):
    """Content route definition"""

    @requires_auth
    def get(self):
        try:
            image_url = "https://cloud.appwrite.io/v1/storage/buckets/64e5cc958cab7d04ed70/files/648ebcac-0a4a-48ec-abd5-350ed839540d/view?project=64e5c98a5b64fe8eac18"

            image_capture_salesforce = get_image_capture(ImageToTextModels.SALESFORCE.value, image_url)
            image_capture_microsoft = get_image_capture(ImageToTextModels.MICROSOFT.value, image_url)
            image_capture_nlpconnect = get_image_capture(ImageToTextModels.NLPCONNECT.value, image_url)

            response = {
                "salesforce": image_capture_salesforce,
                "microsoft": image_capture_microsoft,
                "nlpconnect": image_capture_nlpconnect,
            }

            return response

        except Exception as e:
            return {"success": False, "message": str(e)}, ErrorResponse.BAD_REQUEST.value


class ImageToTextModel:
    """Image to text model definition"""

    def __init__(self, model_name):
        self.captioner = pipeline("image-to-text", model=model_name, max_new_tokens=512)

    def predict(self, image_url):
        """Predict method"""
        return self.captioner(image_url)


def get_image_capture(model_name, image_url):
    """Get image capture method"""

    captioner = ImageToTextModel(model_name)
    image_capture = captioner.predict(image_url)
    return image_capture.pop().get("generated_text")
