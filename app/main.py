from fastapi import FastAPI
from .views import auth_view, post_view
from .db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_view.router, prefix="/auth", tags=["auth"])
app.include_router(post_view.router, prefix="/posts", tags=["posts"])
