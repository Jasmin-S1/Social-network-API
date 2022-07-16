from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


# necemo importovati app objekat vec koristiti APIRouter, i @app.post --> @router.post i tako dalje
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)  
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password) 
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist")
    return user


# sva logika oko hash-iranja passworda se moze premjestiti u "util.py". Util file je zbirka malih funkcija i klasa
# kreiranje route-a za vracanje informacija o pojedinacnom user-u. Npr kod twitera za vracanje informacija o profilu