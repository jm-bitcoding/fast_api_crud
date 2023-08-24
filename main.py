from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hashing import Hash
from oauth2 import get_current_user

import authentication

import models
import schemas

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_user", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    user = models.User(email=user.email, password=Hash.bcrypt(user.password), full_name=user.full_name, is_active=user.is_active)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.post("/student", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, session: Session = Depends(get_session)):
    stu = models.Student(name=student.name, email=student.email, roll_no=student.roll_no)

    session.add(stu)
    session.commit()
    session.refresh(stu)

    return stu


@app.get("/student", response_model=List[schemas.Student])
def all_student(get_current_user: schemas.User = Depends(get_current_user)):
    session = Session(bind=engine, expire_on_commit=False)
    students = session.query(models.Student).all()

    session.close()

    return students


@app.get("/student/{id}")
def get_student(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    stu = session.query(models.Student).get(id)

    session.close()

    if not stu:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"student with {id} not found.")

    return stu


@app.put("/student/{id}")
def update_student(id: int, name: str, email: str, roll_no: str):
    session = Session(bind=engine, expire_on_commit=False)

    stu = session.query(models.Student).get(id)
    if stu:
        stu.name = name
        stu.email = email
        stu.roll_no = roll_no

        session.commit()

    session.close()

    if not stu:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"student with {id} not found.")

    return stu


@app.delete("/student/{id}")
def delete_student(id: int):
    session = Session(bind=engine, expire_on_commit=False)    

    stu = session.query(models.Student).get(id)
    if stu:
        session.delete(stu)
        session.commit()
    
    session.close()

    if not stu:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"student with {id} not found.")
    
    return f"id {id} student is about to be deleted."
