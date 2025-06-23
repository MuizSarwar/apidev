## This file defines the Pydantic models for request and response validation in a FastAPI application.

from pydantic import BaseModel , EmailStr
from datetime import datetime 




# Define a Pydantic model for the post data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  



# Create a Pydantic model for the response data(response validation and serialization)
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created: datetime

    class Config:
        from_attributes = True  





# Create a Pydantic model for the user data
class userCreate(BaseModel):
    email: EmailStr
    password: str




# Create a Pydantic model for the user response data
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        from_attributes = True
