from .config import settings
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from .database import get_db
from sqlalchemy.orm import Session
from . import models,schemas
from datetime import timedelta,datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Create a token for the user to get access to the details

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode_jwt


def verify_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM)
        id:str = payload.get("owner_id")
        if (id is None):
            raise credential_exception
        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        print(e)
        raise credential_exception

    return token_data


def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
   credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

   token = verify_token(token,credential_exception)
   user = db.query(models.User).filter(models.User.id == token.id).first()
   if user is None:
        raise credential_exception
   return user