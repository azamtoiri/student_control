import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base


class Subjects(Base):
    __tablename__ = 'subjects'
    __table_args__ = {
        'comment': 'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов'
    }

    subject_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                        comment='Идентификатор предмета')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Идентификатор пользователя')
    subject_name = Column(String, nullable=False, comment='Название предмета')
    short_description = Column(String, nullable=False, comment='Краткое описание предмета')
    description = Column(String, nullable=False, comment='Полное описание предмета')
    subject_image = Column(String, nullable=False, default='subject_image.png', server_default='subject_image.png',
                           comment='Изображения для предмета')

    enrollments = relationship('Enrollments', backref='subject', cascade='all, delete-orphan')
    subject_tasks = relationship('SubjectTasks', back_populates='subject', cascade='all, delete-orphan')
    subject_theory = relationship(
        'SubjectTheory', uselist=False, back_populates='subject', cascade='all, delete-orphan'
    )

    users = relationship('Users', back_populates='subjects')
