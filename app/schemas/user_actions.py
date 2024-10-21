from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
