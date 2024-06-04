import uuid

from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, expression

from database.model_base import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Таблица пользователей'}

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment='User id column')
    last_name = Column(String, comment='Фамилия')
    first_name = Column(String, comment='Имя')
    middle_name = Column(String, comment='Отчество')
    age = Column(Integer)
    group = Column(String)
    course = Column(Integer, comment='Курс обучения')
    email = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, comment='уникальное Имя пользователя')
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, server_default=expression.false(), default=False,
                      comment='является ли пользователь частью персонала (преподаватель)')
    is_superuser = Column(Boolean, server_default=expression.false(), default=False,
                          comment='является ли пользователь суперпользователем')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                        comment='Дата создания пользователя')
    user_image = Column(String, server_default='default_user_image.png', default='default_user_image.png',
                        comment='Изображение пользователя')

    enrollments = relationship('Enrollments', backref='users', cascade='all, delete-orphan, delete')
    subjects = relationship('Subjects', back_populates='users', cascade='all, delete-orphan')
    user_theme = relationship(
        'UserTheme', back_populates='users', cascade='all, delete-orphan', uselist=False
    )
    teacher_info = relationship(
        'TeacherInformation', back_populates='user', cascade='all, delete-orphan', uselist=False
    )
