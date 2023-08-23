from fastapi import FastAPI, status, HTTPException
from database import Base, engine, Student
from pydantic import BaseModel
from sqlalchemy.orm import Session


class StudentRequest(BaseModel):
    name: str
    email: str
    roll_no: int


Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/student", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentRequest):
    session = Session(bind=engine, expire_on_commit=False)
    stu = Student(name=student.name, email=student.email, roll_no=student.roll_no)

    session.add(stu)
    session.commit()

    id = stu.id
    session.close()

    return f"created student with id {id}."


@app.get("/student")
def all_student():
    session = Session(bind=engine, expire_on_commit=False)
    students = session.query(Student).all()

    session.close()

    return students


@app.get("/student/{id}")
def get_student(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    stu = session.query(Student).get(id)

    session.close()

    if not stu:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"student with {id} not found.")

    return stu


@app.put("/student/{id}")
def update_student(id: int, name: str, email: str, roll_no: str):
    session = Session(bind=engine, expire_on_commit=False)

    stu = session.query(Student).get(id)
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

    stu = session.query(Student).get(id)
    if stu:
        session.delete(stu)
        session.commit()
    
    session.close()

    if not stu:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"student with {id} not found.")
    
    return f"id {id} student is about to be deleted."



