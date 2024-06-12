from typing import Type

from sqlalchemy import select

from database.engine.base_async import AsyncBaseDatabase
from database.models import Task


class TaskRepository(AsyncBaseDatabase):
    async def get_all_user_tasks(self, user_id) -> list[Type[Task]]:
        try:
            async with self._async_session() as session:
                query = await session.execute(select(Task).filter(Task.user_id == user_id))
                return query.scalars().all()
        except Exception as ex:
            print(ex)

    async def add_task(self, task_name, completed: bool, user_id) -> Task | bool:
        async with self._async_session() as session:
            try:
                task = Task(
                    task_name=task_name, completed=completed, user_id=user_id
                )
                session.add(task)
                await session.commit()
                return task
            except Exception as ex:
                print(ex)
                await session.rollback()  # Откат изменений в случае ошибки
                return False

    async def get_task_by_id(self, _id) -> Type[Task]:
        async with self._async_session() as session:
            query = await session.execute(select(Task).filter(Task.task_id == _id))
            return query.scalar()

    async def delete_task(self, task_id) -> bool:
        async with self._async_session() as session:
            task = await self.get_task_by_id(task_id)
            await session.delete(task)
            await session.commit()
            return True

    async def clear_all_tasks(self, user_id) -> bool:
        async with self._async_session() as session:
            tasks = await self.get_all_user_tasks(user_id)
            for task in tasks:
                await session.delete(task)
            await session.commit()
            return True

    async def set_status(self, task_id, status) -> bool:
        async with self._async_session() as session:
            task = await self.get_task_by_id(task_id)
            task.completed = status
            session.add(task)
            await session.commit()
            return True

    async def updated_task(self, task_id, new_task_value) -> bool:
        async with self._async_session() as session:
            task = await self.get_task_by_id(task_id)
            task.task_name = new_task_value
            session.add(task)
            await session.commit()
            return True

    async def get_count_of_tasks(self, user_id) -> int:
        async with self._async_session() as session:
            query = await session.execute(select(Task).filter(Task.user_id == user_id, Task.completed == False))
            tasks = query.scalars().all()
            return len(tasks)
