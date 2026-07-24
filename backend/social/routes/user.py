from fastapi import Depends, HTTPException,APIRouter,status
from ..database import get_db
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError  
# crucial for catching errors that is when a user already has an account




router = APIRouter(
    tags=['Users'],
    prefix="/user"
)

@router.post("/",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def new_user_registeration(user:schemas.NewUser,db:Session = Depends(get_db)):
    new_data = user.model_dump()
    
    new_data["password"] = utils.hash(user.password)

    new_user_models = models.User(**new_data)
    try:
        db.add(new_user_models)
        db.commit()
        db.refresh(new_user_models)
        return new_user_models
    except IntegrityError:
        db.rollback()
        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Registration failed. Email or Username is already taken."
        )
    

@router.get("/me",response_model=schemas.UserResponse)
def get_user (current_user: models.User =Depends(oauth2.get_current_user)):
    return current_user
    

