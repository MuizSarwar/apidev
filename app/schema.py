from pydantic import BaseModel
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
        orm_mode = True

