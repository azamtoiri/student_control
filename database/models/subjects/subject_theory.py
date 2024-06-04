import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base


class SubjectTheory(Base):
    __tablename__ = 'subject_theory'
    __table_args__ = {'comment': 'Теория для предмета. У каждого предмета может быть только одна теория в виде файла'}

    theory_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'), primary_key=True,
                       comment='Идентификатор теории')
    theory_data = Column(String, nullable=True, comment='Данные теории (файл, текст, ссылка)')

    subject = relationship('Subjects', back_populates='subject_theory', uselist=False)
