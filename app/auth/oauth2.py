import os
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from app.db.postgres_connection import get_db
from ..db import user_actions


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY') 
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
 
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt
 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("username")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  user = user_actions.get_user_by_username(db, username=username)
  if user is None:
    raise credentials_exception
  return user