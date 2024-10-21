from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import time
from google.generativeai import GenerativeModel
from .db.models import CommentReply, Comment
from .schemas.comment_reply import CommentReplyCreate

model = GenerativeModel("gemini-1.5-flash")

def generate_auto_reply(comment_content: str, post_content: str) -> str:
    response = model.generate_content(f" Користувач на цей пост: '{post_content}' написав: '{comment_content}', дай йому відповідь")
    return response.text

def schedule_auto_reply(db: Session, comment_id: int, post_content: str, delay: int, background_tasks: BackgroundTasks):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    background_tasks.add_task(
        create_auto_reply_after_delay, db, comment.content, post_content, comment_id, delay
    )

def create_auto_reply_after_delay(db: Session, comment_content: str, post_content: str, comment_id: int, delay: int):
    time.sleep(delay)
    reply_content = generate_auto_reply(comment_content, post_content)
    
    new_reply = CommentReply(
        content=reply_content,
        comment_id=comment_id
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
