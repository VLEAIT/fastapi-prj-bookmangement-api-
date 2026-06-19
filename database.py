from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from loadenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

sessionlocal=sessionmaker( 
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()        

