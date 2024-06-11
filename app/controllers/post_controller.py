from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.post import Post
from app.models.schemas.post import PostCreate
from app.utils import get_current_user


def create_post(db: Session, post: PostCreate, current_user):
    new_post = Post(text=post.text, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_user_posts(db: Session, current_user):
    return db.query(Post).filter(Post.user_id == current_user.id).all()


def delete_post(db: Session, post_id: int, current_user):
    post = db.query(Post).filter(Post.id == post_id,
                                 Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
