from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func, expression

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
    is_staff = Column(Boolean, server_default=expression.false(), default=False)
    is_superuser = Column(Boolean, server_default=expression.false(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now())
    user_image = Column(String, server_default='default_user_image.png', default='default_user_image.png')

    enrollments = relationship('Enrollments', backref='users', cascade='all, delete-orphan, delete')
    subjects = relationship('Subjects', backref='users', cascade='all, delete-orphan')
    user_theme = relationship('UserTheme', back_populates='users', cascade='all, delete-orphan', uselist=False)


class UserTheme(Base):
    __tablename__ = 'user_theme'
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    theme = Column(String, nullable=False, server_default='light', default='light')
    seed_color = Column(String, nullable=False, server_default='green', default='green')

# class Topics(Base):
#     __tablename__ = 'topics'
#     topic_id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     topic_name = Column(String, unique=True, nullable=False)
#     topic_task_id = Column(String, unique=True, nullable=False)
    users = relationship('Users', back_populates='user_theme')

class SubjectTasks(Base):
    __tablename__ = 'subject_tasks'
    subject_task_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    task_name = Column(String, nullable=False, unique=True)
    completed = Column(Boolean, server_default=expression.false(), default=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'))


class Subjects(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    subject_name = Column(String)
    short_description = Column(String, nullable=False)
    description = Column(String, nullable=False)

    enrollments = relationship('Enrollments', backref='subject', cascade='all, delete-orphan')
    subject_tasks = relationship('SubjectTasks', backref='subject', cascade='all, delete-orphan')
    subject_theory = relationship('SubjectTheory', uselist=False, back_populates='subject',
                                  cascade='all, delete-orphan')


class Grades(Base):
    __tablename__ = 'grades'

    grade_id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'))
    grade_value = Column(Integer)
    grade_date = Column(DateTime(timezone=True), server_default=func.now(), default=func.now())


# todo: Date time now for creating
class Enrollments(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'))
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    completed = Column(Boolean, server_default=expression.false(), default=False)


class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String, nullable=False)
    completed = Column(Boolean, server_default=expression.false(), default=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)


class CompletedTaskStatus(Base):
    __tablename__ = 'completed_task_status'

    subject_task_id = Column(Integer, ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'), nullable=False,
                             primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    completed = Column(Boolean, default=False, server_default=expression.false(), nullable=False)

    subject_task = relationship('SubjectTasks', backref='completed_task_status', cascade='all')
    user = relationship('Users', backref='completed_task_status', cascade='all')
