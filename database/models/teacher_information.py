import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.model_base import Base


class TeacherInformation(Base):
    __tablename__ = 'teacher_information'
    __table_args__ = {
        "comment": "Дополнительная информация о преподавателе"
    }

    teacher_information_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                    comment='идентификатор информации')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='id пользователя')
    teacher_experience = Column(Integer, nullable=True, comment='опыт преподавателя')
    teacher_description = Column(String, nullable=True, comment='Информация о преподавателе')
    is_done = Column(Boolean, nullable=False, default=False, server_default=expression.false())

    user = relationship('Users', back_populates='teacher_info')
