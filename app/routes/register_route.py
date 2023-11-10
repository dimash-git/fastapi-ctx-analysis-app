from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models.user_model import User
from ..schema.user_schema import UserCreate, UserResponse
from ..utils.hashing import Hasher

router = APIRouter(tags=['Registration'])


@router.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = Hasher.get_password_hash(user.password)

    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": UserResponse.model_validate(new_user)}


