from werkzeug.exceptions import Unauthorized


def auth(func):
    def wrapper(self):
        if not False:
            raise Unauthorized("You are not authorized to access this resource")
        return func(self)

    return wrapper
