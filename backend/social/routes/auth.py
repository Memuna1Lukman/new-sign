from fastapi import HTTPException,Depends,status,APIRouter
from .. import models,utils,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags= ["Logs"],
    prefix="/login"
)

@router.post("/")
def login_user(user:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
   
    query_username = db.query(models.User).filter(models.User.email == user.username).first()
    if not query_username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
    verify_password = utils.unhash_password(user.password,query_username.password)
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
    )
    
    access_token = oauth2.create_token(data={"owner_id": query_username.id}) 
    return {"token": access_token,"token_type":"bearer"}    