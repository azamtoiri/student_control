from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
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

    enrollments = relationship('Enrollments', backref='users', cascade='all, delete-orphan, delete')


# class Topics(Base):
#     __tablename__ = 'topics'
#
#     topic_id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     topic_name = Column(String, unique=True, nullable=False)


class Subjects(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String)
    # short_description = Column(String)
    description = Column(String)
    # topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=True)

    enrollments = relationship('Enrollments', backref='subject', cascade='all')


class Grades(Base):
    __tablename__ = 'grades'

    grade_id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'))
    grade_value = Column(Integer)
    grade_date = Column(DateTime(timezone=True), server_default=func.now())
    # topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=True)


# todo: Date time now for creating
class Enrollments(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'))
    # is_done = Column(Boolean, default=False) # for done or not subject
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())


class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
