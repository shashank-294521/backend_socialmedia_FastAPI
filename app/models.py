from app.database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,ForeignKey,PrimaryKeyConstraint,DateTime,Text,UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import func
class Post(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    user=relationship("User")



class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Vote(Base):
    __tablename__="votes"

    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)

    # __table_args__=(PrimaryKeyConstraint('post_id','user_id'))

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    edited = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String, nullable=True)  # store filename only
    created_at = Column(DateTime(timezone=True), server_default=func.now())


from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

#     user = relationship("User", back_populates="comments")
#     post = relationship("Post", back_populates="comments")


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Prevent duplicate follows (same follower → following pair)
    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="unique_follow"),)

# Update User model
class User(Base):
    __tablename__ = "users"
    # your existing fields...

    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        backref="following_user",
        cascade="all, delete-orphan"
    )
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        backref="follower_user",
        cascade="all, delete-orphan"
    )