from fastapi import APIRouter, BackgroundTasks, Depends

from sqlalchemy.orm.session import Session

from app.db import user_actions
from app.db.postgres_connection import get_db
from app.auth.oauth2 import get_current_user
from app.schemas.user_actions import UserCreate, UserBase
from app.schemas.posts import PostResponse, PostCreate, PostUpdate
from app.schemas.comment import CommentResponse, CommentCreate


router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('', response_model=UserBase)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return user_actions.create_user(db, request)

@router.post('/posts', response_model=PostResponse)
def create_post(request: PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return user_actions.create_post(db, request, current_user)

@router.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return user_actions.delete_post(post_id, db, current_user)

@router.put('/posts/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return user_actions.update_post(post_id, post_update, db, current_user)

@router.get("/post/{post_id}", response_model=PostResponse)
def get_post(post_id, db: Session = Depends(get_db)):
    return user_actions.get_post(post_id, db)

@router.post('/comment', response_model=CommentResponse)
def create_comment(
        request: CommentCreate, 
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db), 
        current_user: dict = Depends(get_current_user)):
    return user_actions.create_comment(db, request, current_user, background_tasks)

@router.delete('/comment/{comment_id}')
def delete_post(comment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return user_actions.delete_comment(comment_id, db, current_user)

@router.get('/posts/{post_id}/comments', response_model=list[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return user_actions.get_comments_by_post_id(db, post_id)

@router.get('/comments-daily-breakdown')
def comments_daily_breakdown(date_from: str, date_to: str, db: Session = Depends(get_db)):
    return user_actions.get_comments_daily_breakdown(db, date_from, date_to)