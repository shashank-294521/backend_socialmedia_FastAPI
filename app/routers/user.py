from app import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router=APIRouter(
    tags=["Users"]
)

@router.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):

    # hashing the password =user.password

    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

    except Exception as Error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already registered")
    
    return new_user


@router.get("/user/{id}",response_model=schemas.UserOut)
def get_user(id: int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} does not found")
    
    return user
    
