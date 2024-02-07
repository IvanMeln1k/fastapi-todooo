from datetime import UTC, datetime, timedelta
import string
import random

from jwt import encode as jwt_encode, decode as jwt_decode
from jwt.exceptions import  ExpiredSignatureError, InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import Depends

from src.config import SECRET_KEY, ALGORITHM
from src.oauth2_scheme import oauth2_scheme
from src.config import EXP_ACCESS, EXP_EMAIL


def create_random_string():
    letters = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters) for _ in range(32))
    return rand_string


class ExpiredPeriodConfirmation(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Period confirmation expired")


class ExpiredAccessToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Expired access token")


def create_jwt_token(payload: dict):
    return jwt_encode(payload, SECRET_KEY, ALGORITHM)


def get_payload_from_jwt_token(token: str):
    return jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_email_confirmation_token(id: str):
    return create_jwt_token({
        "type": "email confirmation",
        "user_id": id,
        "exp": datetime.now(tz=UTC) + EXP_EMAIL
    })


def get_id_from_email_confirmation_token(token: str):
    try:
        payload = get_payload_from_jwt_token(token)
        return get_id_from_payload(payload, "email confirmation")
    except ExpiredSignatureError:
        raise ExpiredPeriodConfirmation
    except InvalidTokenError:
        raise HTTPException(status_code=500, detail="Server error")


def create_user_id_token(id: int):
    return create_jwt_token({
        "type": "auth",
        "user_id": id,
        "exp": datetime.now(tz=UTC) + EXP_ACCESS
    })


def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = get_payload_from_jwt_token(token)
        return get_id_from_payload(payload, "auth")
    except ExpiredSignatureError:
        raise ExpiredAccessToken
    except InvalidTokenError:
        raise HTTPException(status_code=500, detail="Server error")


def get_id_from_payload(payload: dict, type: str):
    if not "type" in payload or not "user_id" in payload:
        raise HTTPException(status_code=500, detail="Server error")
    elif payload.get("type") == type:
        return payload.get("user_id")
    else:
        raise HTTPException(status_code=500, detail="Server error")
