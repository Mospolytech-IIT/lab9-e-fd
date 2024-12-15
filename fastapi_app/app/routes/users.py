from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.app import schemas, database, crud

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(database.get_db)):
    return crud.get_users(db=db)
