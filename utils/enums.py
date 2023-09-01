from enum import Enum


class PythonEnv(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class ErrorResponse(Enum):
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class ImageToTextModels(Enum):
    SALESFORCE = "Salesforce/blip-image-captioning-large"
    MICROSOFT = "microsoft/git-large-coco"
    NLPCONNECT = "nlpconnect/vit-gpt2-image-captioning"
