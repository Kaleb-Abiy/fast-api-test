from pydantic import BaseModel, constr


class PostCreate(BaseModel):
    text: constr(max_length=1024)


class PostOut(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        orm_mode = True
