from flask_restful import reqparse
from utils.helpers import get_token_auth_header, get_current_user_info, add_user_to_database_if_not_exists


def requires_auth(func):
    parser = reqparse.RequestParser()
    parser.add_argument("Authorization", type=str, location="headers", required=True, help="Bearer token is required")

    def wrapper(self):
        args = parser.parse_args()
        access_token = get_token_auth_header(args.get("Authorization"))
        current_user = get_current_user_info(access_token)
        add_user_to_database_if_not_exists(current_user)
        self.current_user = current_user
        return func(self)

    return wrapper
