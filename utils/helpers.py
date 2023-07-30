import json
from jose import jwt
from six.moves.urllib.request import urlopen
from werkzeug.exceptions import Unauthorized
from config import AUTH0_DOMAIN, AUTH0_API_AUDIENCE, AUTH0_RS256_ALGORITHMS


def get_token_auth_header(access_token):
    if not access_token:
        raise Unauthorized("Authorization header is expected")

    parts = access_token.split()

    if parts[0].lower() != "bearer":
        raise Unauthorized("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Unauthorized("Token not found")
    elif len(parts) > 2:
        raise Unauthorized("Authorization header must be Bearer token")

    token = parts[1]
    return token


def get_current_user(token):
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    try:
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0_RS256_ALGORITHMS,
                audience=AUTH0_API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )
            return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token is expired")
    except jwt.JWTClaimsError:
        raise Unauthorized("Incorrect claims, please check the audience and issuer")
    except Exception:
        raise Unauthorized("Unable to parse authentication token")
