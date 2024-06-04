import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base


class SubjectTasks(Base):
    __tablename__ = 'subject_tasks'
    __table_args__ = {'comment': 'Задания для предмета. У каждого предмета может быть несколько заданий'}

    subject_task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                             comment='Идентификатор задания')
    task_name = Column(String, nullable=False, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'),
                        comment='Идентификатор предмета')

    task_files = relationship('UserTasksFiles', backref='subject_task', cascade='all, delete-orphan', uselist=False)
    subject = relationship('Subjects', back_populates='subject_tasks')
