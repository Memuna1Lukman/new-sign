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
    # 1. Check if user exists
    # 2. Prevent password login for accounts created purely via Google OAuth (password is None)
    if not query_username or query_username.password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    verify_password = utils.unhash_password(user.password,query_username.password)
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
    )
    
    access_token = oauth2.create_token(data={"owner_id": str(query_username.id)}) 
    return {"token": access_token,"token_type":"bearer"}    