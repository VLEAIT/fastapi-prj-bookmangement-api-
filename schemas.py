from pydantic import BaseModel,Field,EmailStr,model_validator
from typing import Optional,literal
from fastapi import FastAPI

class BookCreate(BaseModel):
    title:str=Field(min_length=0,max_length=200)
    author:str
    pages:int=Field(gt=0)
    price:float=Field(ge=0)
    description:Optional[str]=None

class BookResponse(BookCreate):
    id:int
    model_config={"from_attributes":True}

class BookUpdate(BaseModel):
    title:Optional[str]=Field(None,min_length=0,max_length=200)
    author:Optional[str]=None
    pages:Optional[int]=Field(None,gt=0)
    price:Optional[float]=Field(None,ge=0)
    description=Optional[str]=None


class UserBase(BaseModel):
    id:int
    username:str=Field(min_length=6,max_length=20)
    full_name:str
    is_active:bool=Field(default=True)
    email:EmailStr

    @field_validator("username")
    @classmethod
    def validate_username(cls,v:str)->str:
        v=v.strip()
        if " " in v:
            raise ValueError("no space allowed")
        return v    

class UserCreate(UserBase):
    password:str=Field(min_length=8,max_length=20)
    confirm_password:str=Field(min_length=8,max_length=20)

    @model_validator(mode="after")
    def hashed_password(self):
        if self.password!=self.confirm_password:
            raise ValueError("Password no conform")
            return self


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserUpdate(BaseModel):
    username=Optional[str]=Field(None,min_length=6,max_length=20)
    full_name=Optional[str]=None
    is_active=Optional[bool]=None
    email=Optional[EmailStr]=None

    @field_validator("username")
    @classmethod
    def verify_username(cls,v:str)->str:
        v=v.strip()
        if " " in v:
            raise ValueError("no space allowed") 
        return v    

class UserPasswordUpdate(BaseModel):
    old_password:
 
    

    
