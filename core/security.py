from passlib.context import CryptoContext
from datetime import timedelta,datetime,timezone
from jose import JWTError,jwt
from typing import Optional
import os
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from core import hashed_password,verify_password,create_token
  

pwd_context=CryptoContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt_handle_long_password=True
)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
TOKEN_EXPIRE_MINUTES=30


def hashed_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(plain:str,hashed:str)->bool:
    return pwd_context.verify(plain,hashed)

def create_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+ timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode(token:str)->Optional[dict]:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None    

oauth2_scheme=OAuth2PasswordBearer(tokenURL="/auth/login")

def get_current_user(token:str=Depends(oauth2_scheme),db:session=Depends(get_db))->User:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not valid credentials",
        headers={"WWW-Autenticate":"Bearer"},

    )

    try:
        payload=decode_token(token)
        if not payload:
            raise credentials_exception
        user_id:str=payload.get("sub")
        if not user_id:
            raise credentials_exception
    except(JWTError,ValueError):
        raise credentials_exception

    user:db.query(User).filter(User.id==int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="details not found")
    return user
    
        
        



    






 