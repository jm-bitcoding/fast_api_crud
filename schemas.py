from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    roll_no: int


class Student(BaseModel):
    id: int
    name: str
    email: str
    roll_no: int

    class Config:
        orm_mode = True
