from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from constants import Connection
from database.model_base import Base


class AsyncBaseDatabase:
    def __init__(self):
        async_engine = create_async_engine(
            Connection.ASYNC_DATABASE_URL
        )
        self.engine = async_engine
        self._async_session = async_sessionmaker(
            bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self.engine.dispose()
