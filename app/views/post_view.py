from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas.post import PostCreate
from app.controllers.post_controller import create_post, get_user_posts, delete_post
from app.db import get_db
from app.utils import get_current_user
from cachetools import TTLCache

router = APIRouter()

cache = TTLCache(maxsize=100, ttl=300)


@router.post("/addpost")
def add_post(post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if len(post.text.encode('utf-8')) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload too large")
    new_post = create_post(db, post, current_user)
    return {"post_id": new_post.id}


@router.get("/getposts")
def get_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.email in cache:
        return cache[current_user.email]
    posts = get_user_posts(db, current_user)
    cache[current_user.email] = posts
    return posts


@router.delete("/deletepost/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    delete_post(db, post_id, current_user)
    return {"msg": "Post deleted successfully"}
