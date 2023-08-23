from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0202@localhost/fast_api_crud"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


# Models
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(250), unique=True, index=True)
    roll_no = Column(Integer)
