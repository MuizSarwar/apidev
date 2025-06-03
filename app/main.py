# FastAPI application with PostgreSQL connection and basic CRUD operations
#import necessary libraries

from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# Initialize the FastAPI application
app = FastAPI()


# Define a Pydantic model for the post data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value for published is True




#connect to the database using psycopg and check if the connection is successful
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="apidev",
            user="postgres",
            password="tannu",
            cursor_factory=RealDictCursor
            )
        cur = conn.cursor()
        break  # If connection is successful, break the loop

    except Exception as error:
        print("Error connecting to the database:", error)
        time.sleep(2)  # Wait for 2 seconds before retrying



#create get endpoint for home page 
@app.get("/")
@app.get("/home")
def home():
    return {"message": "Welcome to the Home Page!"}


# create get endpoint for all posts page
@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM posts;")
    posts = cur.fetchall()
    return {"all posts ": posts}


# create get endpoint for latest posts
@app.get("/posts/latest")
def get_latest_posts():
    cur.execute("SELECT * FROM posts ORDER BY created DESC LIMIT 1;")
    latest_post = cur.fetchone()
    return {"latest post is ": latest_post}


# create get endpoint for a specific post
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
    post = cur.fetchone()

    if post is None:    # if post is not found, raise an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {f"Here is the post with ID {post_id}!": post} #if post is found, return the post data



#create post endpoint for creating a new post
@app.post("/posts")
def create_post(post: Post):
    try:
        cur.execute(
            "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;",
            (post.title, post.content, post.published)
        )
        new_post = cur.fetchone()
        conn.commit()  # Commit the transaction to save changes
        return {"message": "Post created successfully!", "post": new_post}
    except Exception as error:
        conn.rollback()     # Rollback the transaction in case of error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating post: {error}")


# create put endpoint for updating a post
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    
    try:
        cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
        existing_post = cur.fetchone()
        if existing_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        cur.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;",
            (post.title, post.content, post.published, post_id)
        )
        updated_post = cur.fetchone()
        conn.commit()  # Commit the transaction to save changes
        return {"message": "Post updated successfully!", "post": updated_post}
    except Exception as error:
        conn.rollback()    # Rollback the transaction in case of error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating post: {error}")



# create delete endpoint for deleting a post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
    post = cur.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    try:
        cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (post_id,))
        deleted_post = cur.fetchone()
        conn.commit()  # Commit the transaction to save changes
        return {"message": "Post deleted successfully!", "post": deleted_post}
    except Exception as error:
        conn.rollback()   # Rollback the transaction in case of error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting post: {error}")


# Close the database connection when the application is shutting down
@app.on_event("shutdown")
def shutdown():
    if conn:
        cur.close()
        conn.close()
        print("Database connection closed.")
        