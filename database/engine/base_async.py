from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from constants import Connection
from database.model_base import Base


class AsyncBaseDatabase:
    def __init__(self):
        self.async_engine = create_async_engine(
            Connection.ASYNC_DATABASE_URL
        )
        self.engine = self.async_engine
        self._async_session = async_sessionmaker(
            bind=self.async_engine, class_=AsyncSession, expire_on_commit=False, future=True
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self.engine.dispose()

    @asynccontextmanager
    async def session_scope(self):
        """
                Асинхронный контекстный менеджер для сессий SQLAlchemy.
        Управляет транзакциями: автоматически коммитит или откатывает транзакции в случае ошибки.

        :return:
        """
        async with self._async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
