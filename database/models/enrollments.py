import uuid

from sqlalchemy import Column, ForeignKey, Boolean, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base
from database.models.grades.task_grades import TaskGrades


class Enrollments(Base):
    __tablename__ = 'enrollments'
    __table_args__ = {'comment': 'Записи о подписках пользователей на предметы'}

    enrollment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                           comment='Идентификатор записи о подписке')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Пользователь, подписавшийся на предмет')
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'), nullable=False,
                        comment='Предмет, на который подписался пользователь. Сам предмет')
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                             comment='Дата подписки')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус завершения предмета')

    task_files = relationship('UserTasksFiles', backref='enrollments', cascade='all, delete-orphan')
    task_grades_list = relationship('TaskGrades', back_populates='enrollment', cascade='all, delete-orphan',
                                    foreign_keys=[TaskGrades.enrollment_id])
