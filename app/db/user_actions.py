from fastapi import BackgroundTasks, HTTPException, status

from sqlalchemy import func, case
from sqlalchemy.orm.session import Session

from app.hash.hashing import Hash
from app.schemas.user_actions import UserCreate
from app.db.models import User, Post, Comment
from app.schemas.posts import PostCreate, PostUpdate
from app.schemas.comment import CommentCreate
from app.gemini.gemini_conf import check_profanity
from app.auto_reply import schedule_auto_reply

def create_user(db: Session, request: UserCreate):
    new_user = User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
    return user

def create_post(db: Session, request: PostCreate, current_user):
    is_blocked = check_profanity(request.content)
    
    new_post = Post(
        title = request.title,
        content = request.content,
        author_id = current_user.id,
        is_blocked = is_blocked
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def delete_post(post_id: int, db: Session, current_user):
    post = db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this post')
    
    db.delete(post)
    db.commit()
    return post

def update_post(post_id: int, post_update: PostUpdate, db: Session, current_user):
    post = db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this post')
    
    is_title_profane = check_profanity(post_update.title)
    is_content_profane = check_profanity(post_update.content)

    if is_title_profane or is_content_profane:
        is_blocked = True
    
    post.title = post_update.title
    post.content = post_update.content
    post.is_blocked = is_blocked
    db.commit()
    db.refresh(post)
    return post

def get_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    return post

def create_comment(db: Session, request: CommentCreate, current_user, background_tasks: BackgroundTasks):
    post = db.query(Post).filter(Post.id==request.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    is_blocked = check_profanity(request.content)
    
    new_comment = Comment(
        content = request.content,
        post_id = request.post_id,
        author_id = current_user.id,
        is_blocked = is_blocked
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    if post.author.auto_reply_delay > 0:
        schedule_auto_reply(db, new_comment.id, post.content, post.author.auto_reply_delay, background_tasks)

    return new_comment

def delete_comment(comment_id: int, db: Session, current_user):
    comment = db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if comment.author_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this post')
    
    db.delete(comment)
    db.commit()
    return comment

def get_comments_by_post_id(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def get_comments_daily_breakdown(db: Session, date_from: str, date_to: str):
    results = (
        db.query(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id).label("total_comments"),
            func.sum(case((Comment.is_blocked == True, 1), else_=0)).label("blocked_comments")
        )
        .filter(Comment.created_at >= date_from, Comment.created_at <= date_to)
        .group_by(func.date(Comment.created_at))
        .order_by(func.date(Comment.created_at)) 
        .all()
    )
    
    return [
        {
            "date": row.date,
            "total_comments": row.total_comments,
            "blocked_comments": row.blocked_comments
        }
        for row in results
    ]