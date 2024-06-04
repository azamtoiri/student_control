from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base


class UserTasksFiles(Base):
    __tablename__ = 'user_task_files'
    __table_args__ = {
        'comment': 'Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов'
    }

    subject_task_id = Column(UUID(as_uuid=True), ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'),
                             nullable=False, primary_key=True, comment='Идентификатор задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     primary_key=True, comment='пользователь')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=False, comment='предмет на который записан пользователй')
    task_file = Column(String, nullable=False, comment='файл прикрепленный к заданию')
    completed = Column(Boolean, nullable=False, default=True, server_default=expression.true(),
                       comment='Отправил ли ученик задание')

    user = relationship('Users', backref='user_task_files')
