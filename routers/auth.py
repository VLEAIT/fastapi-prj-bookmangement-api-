from fastapi import HTTPException,APIRouter,Depends,status
from database import get_db
from models import User
from schemas import UserResponse,UserCreate,UserLogin
from sqlalchemy.orm import Session


router=APIRouter(
    preflix="/auth",
    tags=["auth"]
)

#registration
@router.post("/register",response_model=UserResponse,status_code=201)
def register(user:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="no data")
    hashed=hashed_password(user.password)
    db_user=User(**user.model_dump(exclude={"password","confirm_password"}),password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
#login
@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if not existing or not verify_password(user.password,existing.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="the value is not authorized")
    token=create_token({"sub":str(existing.id)}) 
    return {"access_token":token,"token_type":"bearer"}  


