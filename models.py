from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,Text,DateTime,Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True,nullable=False)
    email=Column(String,unique=True,nullable=False,index=True)
    password=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    full_name=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    books=relationship("Book",back_populates="owner")
 

class Book(Base):
    __tablename__="books"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    author=Column(String,nullable=False)
    pages=Column(Integer)
    price=Column(Float)
    description=Column(Text,nullable=False)
    owner_id=Column(Integer,ForeignKey("users.id"))
    created_id=Column(DateTime(timezone=True),server_default=func.now())
  
    owner=relationship("User",back_populates="books")

       





