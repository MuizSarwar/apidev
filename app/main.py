# FastAPI application with PostgreSQL connection and basic CRUD operations
#import necessary libraries

from fastapi import FastAPI,HTTPException, status, Depends
from . import models
from .database import engine, get_db 
from sqlalchemy.orm import Session
from . import schema,utils
from .routers import home,post, user






# Create tables in the database if they don't exist
models.Base.metadata.create_all(bind=engine)  


# Initialize the FastAPI application
app = FastAPI()





app.include_router(home.router)
app.include_router(post.router)
app.include_router(user.router)





