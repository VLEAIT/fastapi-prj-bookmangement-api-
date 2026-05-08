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


