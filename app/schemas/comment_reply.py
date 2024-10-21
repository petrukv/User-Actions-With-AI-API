from pydantic import BaseModel
from datetime import datetime

class CommentReplyBase(BaseModel):
    content: str

class CommentReplyCreate(CommentReplyBase):
    comment_id: int

class CommentReplyResponse(CommentReplyBase):
    id: int
    comment_id: int
    created_at: datetime

    class Config:
        from_attributes = True
