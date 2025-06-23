from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import  get_db




router = APIRouter(
    prefix="/users",
    tags=["Users"],
)





# create post endpoint for creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user:schema.userCreate,  db: Session = Depends(get_db)):
    
    # Hash the password before storing it
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    try:
        new_user = models.User(**user.dict())  
        db.add(new_user)  
        db.commit()  
        db.refresh(new_user)  
        return new_user  
    
    except Exception as error:
        db.rollback() 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {error}")
    



# create get endpoint for one user
@router.get("/{user_id}", response_model=schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()  

    if user is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


