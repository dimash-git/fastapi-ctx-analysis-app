from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..dependencies import get_db, has_token
from ..models import post_model
from ..schema import post_schema
from ..database import engine

# post_model.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=['Posts'])


@router.post("/api/posts/", response_model=post_schema.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: post_schema.PostBase, db: Session = Depends(get_db), user_id: int = Depends(has_token)):
    post_data = post.model_dump()
    post_data["user_id"] = user_id
    db_post = post_model.Post(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/api/posts/", response_model=list[post_schema.Post], status_code=status.HTTP_200_OK)
def get_posts(skip: int = 0,
              limit: int = 100,
              db: Session = Depends(get_db),
              user_id: int = Depends(has_token)):
    posts = db.query(post_model.Post).filter(post_model.Post.user_id == user_id).offset(skip).limit(limit).all()
    return posts


@router.get("/api/posts/{post_id}", response_model=post_schema.Post, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(has_token)):
    db_post = db.query(post_model.Post).filter(post_model.Post.user_id == user_id,
                                               post_model.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/api/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(has_token)):
    db_post = db.query(post_model.Post).filter(post_model.Post.user_id == user_id,
                                               post_model.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted"}


@router.put("/api/posts/{post_id}", response_model=post_schema.Post, status_code=status.HTTP_200_OK)
def update_post(post_id: int,
                post: post_schema.Post,
                db: Session =
                Depends(get_db), user_id: int = Depends(has_token)):
    db_post = db.query(post_model.Post).filter(post_model.Post.user_id == user_id,
                                               post_model.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.title = post.title
    db_post.description = post.description
    db.commit()
    db.refresh(db_post)
    return db_post
