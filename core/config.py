from fastapi import HTTPException,APIRouter,Depends
from database import get_db
from schemas import UserCreate,UserResponse,
from models import User
from core import hashed_password,verify_password,create_token




router=APIRouter(
    preflix="/auth",
    tags=["auth"]
)
#Register
@router.post("/register",response_model=UserResponse,status_code=201)
def register(user:UserCreate,db:Sessions=Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="no content")
    hashed=hashed_password(password)
    db_user=User(**user.model_dump(exclude:{"password","conform_password"}),password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#login
@router.post("/login")
def login(user:UserLogin,db:Sessions=Depends(get_db)):
    existing =db.query(User).filter(User.email==user.email).first()
    if not existing or not verify_password(user.password,existing.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="the value is not authorized")
    token=create_token({"sub":str(existing.id)})
    return {"acces_token":token,"token_type":"bearer"}    

