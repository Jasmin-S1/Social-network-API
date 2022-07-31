from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class Post(BaseModel):      
    title: str              
    content: str           
    published: bool = True  

class CreatePost(BaseModel):      
    title: str              
    content: str           
    published: bool = True  

class UpdatePost(BaseModel):      
    title: str              
    content: str           
    published: bool

class PostBase(BaseModel):         
    title: str              
    content: str           
    published: bool = True  

class PostCreate(PostBase):   
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase):   
    created_at: datetime      
    user_id: int
    user: UserResponse   

    class Config:
        orm_mode = True

class PostVotes(PostBase):  
    Post: PostResponse    
    votes: int

class UserCreate(BaseModel):
    email: EmailStr          
    password: str           

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)  
