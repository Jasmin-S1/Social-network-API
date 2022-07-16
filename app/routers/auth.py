from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, utils, models, oauth2


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)           #when user send the data in one direction, it is post request
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # umjesto user_credential: schemas.UserLogin koristi se OAuth2PasswordRequestForm
    # koristeci ovaj format vise nema user_credential.email vec user_credential.username
    # OAuth2PasswordRequestForm - ova forma ne uzima u obzir sta je username, to moze biti id, email ili slicno, ona samo kreira field pod nazivom username
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    
    return {"access_token": access_token, "token_type": "bearer"}
