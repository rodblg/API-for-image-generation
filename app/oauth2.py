from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema, models
from config import settings
from database import get_db
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def verify_acces_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = schema.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail='Could not validate credentials', 
                                          headers={'WWW-Authenticate': 'Bearer'})
    
    token = verify_acces_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
