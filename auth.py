from time import time
from jose.jwt import encode, decode
from bcrypt import gensalt, hashpw, checkpw

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from settings import JWT_ALGORITHM, JWT_SECRET, JWT_DURATION_SECS


def create_jwt(user_id: str) -> str:
    return {
        "access_token": encode(
            {"user_id": user_id, "expires": time() + float(JWT_DURATION_SECS)},
            JWT_SECRET,
            JWT_ALGORITHM,
        ),
        "user_id": user_id,
    }


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time() else None
    except:
        return None


def hash_password(passwd: str) -> dict:
    return {
        "hashed_password": hashpw(passwd.encode(), gensalt()).decode(),
    }


def check_password(password: str, hashed_password: str):
    return checkpw(password.encode(), hashed_password.encode())


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
