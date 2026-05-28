from passlib.context import CryptoContext
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
import os
from typing import Optional

pwd=CryptoContext(schemes=["bcrypt"],deprecated="auto",bcrypt_handle_long_passwords=True)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
TOKEN_EXPIRE_MINUTES=30


def hashed_password(password:str)->str:
    return pwd.hash(password)

def verifY_passport(hashed:str,plain:str)->bool:
    return pwd.verify(plain,hashed)

def create_acess_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_token(token:str)->Optional[dict]:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None    







 