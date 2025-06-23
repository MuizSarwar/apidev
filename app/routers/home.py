from fastapi import APIRouter

router = APIRouter()

#create get endpoint for home page 
@router.get("/")
@router.get("/home")
def home():
    return {"message": "Welcome to the Home Page!"}

