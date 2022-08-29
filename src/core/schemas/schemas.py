from pydantic import BaseModel


class UserInfoToken(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: int
    exp: int
    azp: str
    gty: str
