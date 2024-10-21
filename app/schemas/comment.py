from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: int


class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author_id: int
    is_blocked: bool

    class Config:
        from_attributes = True