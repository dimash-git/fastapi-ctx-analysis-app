from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from sqlalchemy.orm import Session
from ..dependencies import get_db, has_token
from ..models.user_model import User
from ..schema.user_schema import UserLogin, UserResponse
from ..utils.hashing import Hasher
from ..utils.jwt_handler import sign_jwt, decode_jwt
from ..utils.token_blacklist import is_token_blacklisted, blacklist_token
from ..config.general_config import APP_PREFIX

router = APIRouter(tags=['Authentication'])

cookie_key = APP_PREFIX + "access_token"


@router.post("/api/auth/login", status_code=status.HTTP_200_OK)
def signin(user: UserLogin, request: Request, response: Response, db: Session = Depends(get_db),):
    db_user = db.query(User).filter(User.email == user.email).first()
    # Find user
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password
    if not Hasher.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = sign_jwt(str(db_user.id))

    old_token = request.cookies.get(cookie_key)
    if old_token and not is_token_blacklisted(old_token):
        blacklist_token(old_token)

    # Set the JWT token in an HTTP-only cookie
    response.set_cookie(key=cookie_key, value=token["access_token"], httponly=True)

    return {"detail": "Logged in successfully."}


@router.post("/api/auth/refresh")
def refresh_token(request: Request, response: Response):
    old_token = request.cookies.get(cookie_key)

    if old_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if is_token_blacklisted(old_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")

    decoded_token = decode_jwt(old_token)
    token = sign_jwt(decoded_token["user_id"])

    response.set_cookie(key=cookie_key, value=token["access_token"], httponly=True)

    return {"detail": "Access token refreshed successfully."}


@router.post("/api/auth/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie(key=cookie_key)
    return {"detail": "Logged out successfully."}


@router.post("/api/auth/me", status_code=status.HTTP_200_OK)
def me(db: Session = Depends(get_db), token=Depends(has_token)):
    user_id = token["user_id"]
    db_user = db.query(User).filter(User.id == user_id).first()
    user = UserResponse.model_validate(db_user)
    return {
        "detail": "User is authenticated.",
        "user": user
    }
