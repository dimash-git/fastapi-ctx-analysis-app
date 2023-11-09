from app.config.general_config import JWT_SECRET, JWT_ALGO
import time
import jwt


# returns generated token
def token_response(token: str):
    return {
        "access_token": token
    }


# encode jwt token and returns it
def sign_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "expires_at": time.time() + 30 * 60  # 30 min
    }
    token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGO)
    return token_response(token)


# decodes jwt token and returns its contents
def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, key=JWT_SECRET, algorithms=JWT_ALGO)
        return decode_token
    except Exception:
        return {}
