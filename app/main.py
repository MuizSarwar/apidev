from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()


# Define a Pydantic model for the post data
class Post(BaseModel):
    title: str
    content: str



#create get endpoint for home page 
@app.get("/")
@app.get("/home")
def home():
    return {"message": "Welcome to the Home Page!"}


# create get endpoint for all posts page
@app.get("/posts")
def get_posts():
    return {"message": "Here are all the posts!"}


# create get endpoint for latest posts
@app.get("/posts/latest")
def get_latest_posts():

    # here we will implement logic to check if there are not any latest posts, then an exception will be raised

    return {"message": "Here are the latest posts!"}


# create get endpoint for a specific post
@app.get("/posts/{post_id}")
def get_post(post_id: int):

    # here we will implement logic to check if the post with the given ID exists, if not, an exception will be raised
    
    return {"message": f"Here is the post with ID {post_id}!"}



#create post endpoint for creating a new post
@app.post("/posts")
def create_post(post: Post):
    return {"message": "Post created successfully!", "post": post.dict()}


# create put endpoint for updating a post
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):

    # here we will implement logic to check if the post with the given ID exists, if not, an exception will be raised

    return {"message": f"Post with ID {post_id} updated successfully!", "post": post.dict()}


# create delete endpoint for deleting a post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):

    # here we will implement logic to check if the post with the given ID exists, if not, an exception will be raised

    return {"message": f"Post with ID {post_id} deleted successfully!"}
