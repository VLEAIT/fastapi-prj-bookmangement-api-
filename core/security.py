from passlib.context import CryptoContext
from datetime import timedelta,datetime,timezone
from json import JWTError,jwt
from typing import Optional
import os

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








 