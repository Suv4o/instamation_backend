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

            captioner_salesforce = ImageToTextModel(ImageToTextModels.SALESFORCE.value)
            image_capture_salesforce = captioner_salesforce.predict(image_url)

            captioner_microsoft = ImageToTextModel(ImageToTextModels.MICROSOFT.value)
            image_capture_microsoft = captioner_microsoft.predict(image_url)

            captioner_nlpconnect = ImageToTextModel(ImageToTextModels.NLPCONNECT.value)
            image_capture_nlpconnect = captioner_nlpconnect.predict(image_url)

            response = {
                "salesforce": image_capture_salesforce.pop().get("generated_text"),
                "microsoft": image_capture_microsoft.pop().get("generated_text"),
                "nlpconnect": image_capture_nlpconnect.pop().get("generated_text"),
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
