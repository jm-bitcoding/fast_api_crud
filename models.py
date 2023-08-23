from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(250), unique=True, index=True)
    roll_no = Column(Integer)
    