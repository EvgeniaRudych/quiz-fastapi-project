import os
import jwt
from configparser import ConfigParser

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

from config import system_config
from core.schemas.schemas import UserInfoToken

token_auth_scheme = HTTPBearer()


# domain = system_config.domain
# algorithms = system_config.algorithms
# audience = system_config.api_audience
# issuer = system_config.issuer
#

class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{system_config.domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):

        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=system_config.algorithms,
                audience=system_config.api_audience,
                issuer=system_config.issuer,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload


# что у меня есть: в пайдентик модель должна записаться инфа с токена. Вопрос: как ее записать туда
# потом я просто отдаю в ретурн это

def get_user_info(token=Depends(token_auth_scheme)):
    try:
        main_info = UserInfoToken(**VerifyToken(token.credentials).verify())

    except ValidationError as error:
        raise HTTPException(status_code=401, detail="Credentials were not provided")

    return main_info

