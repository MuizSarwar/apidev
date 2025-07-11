# In this file, we define the SQLAlchemy models for our application.


from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text



class Post(Base):
    __tablename__ = "posts"

    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)






