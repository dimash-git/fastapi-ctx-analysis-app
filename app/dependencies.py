import time
from fastapi import HTTPException, Request, status
from .config.general_config import APP_PREFIX
from .utils.jwt_handler import decode_jwt
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def has_token(request: Request):
    cookie_key = APP_PREFIX + "access_token"
    token = request.cookies.get(cookie_key)

    print(token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user.")

    decoded_token = decode_jwt(token)

    expires_at = decoded_token["expires_at"]
    if not expires_at or expires_at < time.time():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")

    return int(decoded_token["user_id"])
