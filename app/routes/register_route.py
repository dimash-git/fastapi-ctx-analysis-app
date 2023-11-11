from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import user_model
from ..schema.user_schema import UserCreate, UserResponse
from ..utils.hashing import Hasher
from ..database import engine

# user_model.Base.metadata.create_all(bind=engine)
# user_model.Base.metadata.drop_all(bind=engine)

router = APIRouter(tags=['Registration'])


@router.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = Hasher.get_password_hash(user.password)

    new_user = user_model.User(name=user.name, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": "User created successfully", "user": UserResponse.model_validate(new_user)}


