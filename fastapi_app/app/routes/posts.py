from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_app.app import schemas, database, crud

router = APIRouter()

@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    return crud.create_post(db=db, post=post)
