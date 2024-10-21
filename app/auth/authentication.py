from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from .oauth2 import create_access_token
from app.db.postgres_connection import get_db
from app.hash.hashing import Hash
from app.db.models import User


router = APIRouter(
    prefix='/login',
    tags=['authentication']
)

@router.post("")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Incorrect password')
    
    access_token = create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }