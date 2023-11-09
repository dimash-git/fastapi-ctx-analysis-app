from fastapi import APIRouter, HTTPException

router = APIRouter()

posts = [
    {
        "id": 1,
        "title": "Title 1",
        "content": "Content 1"
    },
    {
        "id": 2,
        "title": "Title 2",
        "content": "Content 2"
    },
    {
        "id": 3,
        "title": "Title 3",
        "content": "Content 3"
    }
]


@router.get("/posts/")
def get_posts():
    return {"data": posts}


@router.get("/posts/{post_id}")
def get_single_post(post_id: int):
    found_post = next((post for post in posts if post["id"] == post_id), None)
    if found_post is None:
        raise HTTPException(status_code=404, detail="Post not found.")
    return {"data": found_post}
