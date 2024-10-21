from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .postgres_connection import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    auto_reply_delay = Column(Integer, nullable=True, default=0)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('Users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_blocked = Column(Boolean, default=False)


    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "Comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('Posts.id'))
    author_id = Column(Integer, ForeignKey('Users.id'))
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    replies = relationship("CommentReply", back_populates="comment")

class CommentReply(Base):
    __tablename__ = "CommentReplies"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    comment_id = Column(Integer, ForeignKey('Comments.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_generated = Column(Boolean, default=True)

    comment = relationship("Comment", back_populates="replies")
