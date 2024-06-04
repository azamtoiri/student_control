from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.model_base import Base


class UserTheme(Base):
    __tablename__ = 'user_theme'
    __table_args__ = {'comment': 'Цветовая схема пользователя (тема). Уникальная для каждого пользователя'}

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True,
                     comment='Идентификатор пользователя')
    theme = Column(String, nullable=False, server_default='light', default='light',
                   comment='Тема пользователя (светлая/темная)')
    seed_color = Column(String, nullable=False, server_default='green', default='green',
                        comment='Цвет цветовой схемы приложения')

    users = relationship('Users', back_populates='user_theme')
