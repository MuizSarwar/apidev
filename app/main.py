# FastAPI application with PostgreSQL connection and basic CRUD operations
#import necessary libraries

from fastapi import FastAPI,HTTPException, status, Depends
from . import models
from .database import engine, get_db 
from sqlalchemy.orm import Session
from . import schema



# Create tables in the database if they don't exist
models.Base.metadata.create_all(bind=engine)  


# Initialize the FastAPI application
app = FastAPI()




#create get endpoint for home page 
@app.get("/")
@app.get("/home")
def home():
    return {"message": "Welcome to the Home Page!"}




# create get endpoint for all posts page
@app.get("/posts", response_model=list[schema.PostResponse])  
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()  
    return posts




# create get endpoint for latest posts
@app.get("/posts/latest", response_model=schema.PostResponse)  
def get_latest_posts(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created.desc()).first()  
    
    if latest_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    return latest_post




# create get endpoint for a specific post
@app.get("/posts/{post_id}", response_model=schema.PostResponse)
def get_post(post_id: int , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()  

    if post is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post




#create post endpoint for creating a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse)
def create_post(post: schema.Post,db: Session = Depends(get_db)):
    try:
        new_post = models.Post(**post.dict())  
        db.add(new_post)  
        db.commit()  
        db.refresh(new_post)  
        return new_post  
    
    except Exception as error:
        db.rollback() 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating post: {error}")






# create put endpoint for updating a post
@app.put("/posts/{post_id}",response_model=schema.PostResponse)
def update_post(post_id: int, updated_post: schema.Post, db: Session = Depends(get_db)):
    
    try:
        post_query = db.query(models.Post).filter(models.Post.id == post_id)
        post = post_query.first()  

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        post.title = updated_post.title
        post.content = updated_post.content
        post.published = updated_post.published
        db.commit()  
        db.refresh(post)
        return post
        
    except Exception as error:
        db.rollback() 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating post: {error}")







# create delete endpoint for deleting a post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    try:
        db.delete(post)  
        db.commit()  
        
    except Exception as error:
        db.rollback()  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting post: {error}")


        