from pydantic import BaseModel,field_validator,model_validator,Field,EmailStr
from typing import Optional


class UserBase(BaseModel):
    username:str=Field(min_length=6,max_length=20)
    full_name:str
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
    username:Optional[str]=Field(None,min_length=6,max_length=20)
    full_name:Optional[str]=None
    is_active:Optional[bool]=None
    email:Optional[EmailStr]=None

    @field_validator("username")
    @classmethod
    def verify_username(cls,v:str)->str:
        v=v.strip()
        if " " in v:
            raise ValueError("no space allowed") 
        return v    
class UserResponse(UserBase):
    id:int
    is_active:bool=Field(default=True)

    model_config={"from_attributes":True}

     