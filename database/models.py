from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean, TIMESTAMP, text, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)  # id
    last_name = Column(String)  # fam
    first_name = Column(String)  # imya
    middle_name = Column(String)  # отчество
    age = Column(Integer)  # let
    group = Column(String)  # группа
    course = Column(Integer)  # курс
    email = Column(String)  # email
    username = Column(String, unique=True)  # username for login
    password = Column(String)  # password for login
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subjects(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String)
    description = Column(String)


class Grades(Base):
    __tablename__ = 'grades'

    grade_id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.enrollment_id'))
    grade_value = Column(Integer)
    grade_date = Column(DateTime(timezone=True), server_default=func.now())


# todo: Date time now for creating
class Enrollments(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
