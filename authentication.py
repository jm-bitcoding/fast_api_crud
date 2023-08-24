from fastapi import status, HTTPException, Depends, APIRouter
from database import get_session
from sqlalchemy.orm import Session
from hashing import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from jwt_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from typing import Annotated

import models

router = APIRouter(tags = ['Authentication'])


@router.post("/login")
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Email")
    
    if not Hash.verify_password(request.password, user.password):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
