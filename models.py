from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, PrimaryKeyConstraint
from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        return "<User {full_name!r}>".format(full_name=self.full_name)
    

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(250), unique=True, index=True)
    roll_no = Column(Integer)
    