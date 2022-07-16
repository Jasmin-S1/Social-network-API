import imp
from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")                      # ovo ce biti endpoint login-a

# Moramo obezbijediti sljedece podatke:
# 1. SECRET_KEY
# 2. Algorithm
# 3. Expriation time

SECRET_KEY = settings.secret_key # ova varijabla i ove ispod se ne pisu u kodu vec se kreiraju environment variable
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() # radi sigurnosti kreiramo kopiju podataka i pohranimo ih u neku varijablu

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # dodaje novi "key" u dictionary "data"

    encodeed_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # pozivanje funkcije koja kreira token
    # to_encode - su podaci za payload, ostalo je definisano

    return encodeed_jwt


def verify_access_token(token: str, credential_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])   # algoritam ide u srednju zagradu zato sto moze biti lista algoritama
        id: str = payload.get("user_id") 

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id= id)
    except JWTError:
        raise credential_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user