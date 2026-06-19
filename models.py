from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Text,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    username=Column(String,index=True,unique=True,nullable=True)
    full_name=Column(String,index=True,unique=True,nullable=True)
    email=Column(String,index=True,unique=True,nullable=True)
    password=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    books=relationship("User",back_populates="users")

class Book(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    author=Column(String,nullable=False)
    pages=Column(Integer,nullable=False)
    description=Column(Text)
    owner_id=Column(Integer,ForeignKey("users.id"))
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    users=relationship("Book",back_populates="books")
       





