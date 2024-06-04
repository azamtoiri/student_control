import uuid

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.model_base import Base


class TaskGrades(Base):
    __tablename__ = 'task_grades'
    __table_args__ = {'comment': 'Оценки за задания по предметам'}

    task_grade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                           comment='Идентификатор оценки за задание')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=True,
                           comment='Идентификатор записи о подписке')
    subject_task_id = Column(UUID(as_uuid=True), ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'),
                             nullable=False, comment='Идентификатор задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Идентификатор пользователя, который выполнил задание')
    grade_value = Column(Integer, nullable=False, comment='Оценка за задание')
    grade_date = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=func.now(),
        comment='Дата постановки оценки'
    )

    enrollment = relationship('Enrollments', back_populates='task_grades_list', foreign_keys=[enrollment_id])
    subject_task = relationship('SubjectTasks', backref='task_grades')
    users = relationship('Users', backref='task_grades')
