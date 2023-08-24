from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    is_active: bool


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    full_name: str
    is_active: bool

    class Config:
        orm_mode = True



class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


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
