from datetime import UTC, datetime, timedelta

from jwt import encode as jwt_encode, decode as jwt_decode
from jwt.exceptions import  ExpiredSignatureError, InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import Depends

from src.config import SECRET_KEY, ALGORITHM
from src.oauth2_scheme import oauth2_scheme


class ExpiredPeriodConfirmation(HTTPException):
    def __init__(self):
        super().__init__(status_code=200, detail="Period confirmation expired")


class UserAccessError(HTTPException):
    def __init__(self):
        super().__init__(status_code=200, detail="User access error")


def create_jwt_token(payload: dict):
    return jwt_encode(payload, SECRET_KEY, ALGORITHM)


def get_payload_from_jwt_token(token: str):
    return jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_email_confirmation_token(email: str,
                                 exp: datetime = datetime.now(tz=UTC) + timedelta(hours=1)):
    return create_jwt_token({
        "email": email,
        "exp": exp
    })


def get_email_from_confirmation_token(token: str):
    """return email from token, if token don't contain email, it returns an error"""
    try:
        payload = get_payload_from_jwt_token(token)
        if "email" in payload:
            return payload.get("email")
        else:
            raise HTTPException(status_code=500, detail="Server error")
    except ExpiredSignatureError:
        raise ExpiredPeriodConfirmation
    except InvalidTokenError:
        raise HTTPException(status_code=500, detail="Server error")


def create_user_id_token(id: int):
    return create_jwt_token({
        "user_id": id
    })


def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = get_payload_from_jwt_token(token)
        if "user_id" in payload:
            return payload.get("user_id")
        else:
            raise HTTPException(status_code=500, detail="Server error")
    except InvalidTokenError:
        raise HTTPException(status_code=500, detail="Server error")