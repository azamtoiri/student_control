import uuid

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from database.model_base import Base


class Grades(Base):
    __tablename__ = 'grades'
    __table_args__ = {'comment': 'Итоговая оценка студентов по предметам'}

    grade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                      comment='Идентификатор оценки')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=False, comment='Идентификатор записи о подписке')
    grade_value = Column(Integer, nullable=False, comment='Сама оценка')
    grade_date = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                        comment='Дата выставления оценки')
