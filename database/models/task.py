import uuid

from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression

from database.model_base import Base


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {
        'comment': 'Todo list. Задания пользователей которые они должны выполнить (цели). '
    }

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                     comment='Идентификатор задания')
    task_name = Column(String, nullable=False, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False,
                     comment='Пользователь которому принадлежит задание')
