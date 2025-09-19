from pydantic import BaseModel,EmailStr, Field
from datetime import datetime
from typing import Optional

# class Post(BaseModel):
#     title:str
#     content:str
#     published : bool=True
#     # review: Optional[int]=None

# class CreatePost(BaseModel):
#     title:str
#     content:str
#     published : bool=True


# class UpdatePost(BaseModel):
#     title:str
#     content:str
#     published : bool

class PostBase(BaseModel):
    # id:int
    title:str
    content:str
    # user_id:int
    published : Optional[bool]=True

class PostCreate(PostBase):

    pass



class UserOut(BaseModel):
    id :int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

# response 
class Post(PostBase):
    id :int
    # title:str
    # content: str
    # published: bool
    user_id:int
    created_at:datetime
    user:UserOut
    

    class Config:
        orm_mode=True


class PostOut(BaseModel):
    post:Post
    votes:int
    class Config:
        orm_mode=True

# user table
class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id :int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True



class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int]=None


class Vote(BaseModel):
    post_id: int
    dir:int=Field(...,ge=0,le=1)


from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageOut(BaseModel):
    
    sender_id: int
    receiver_id: int
    content: str
   

    class Config:
        orm_mode = True


class MessageUpdate(BaseModel):
    content: str


class ProfileBase(BaseModel):
    bio: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    profile_picture_url: Optional[str] = None
    profile_picture_preview: Optional[str] = None  # base64 preview for Swagger

    class Config:
        from_attributes = True


# class CommentBase(BaseModel):
#     content: str

# class CommentCreate(CommentBase):
#     pass

# from pydantic import BaseModel, ConfigDict

# class CommentResponse(BaseModel):
#     id: int
#     content: str
#     user_id: int
#     post_id: int

#     model_config = ConfigDict(from_attributes=True)



class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        orm_mode = True