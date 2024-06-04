from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.database import AsyncBaseDatabase
from database.models import Users, Subjects, Enrollments, SubjectTasks
from utils.exceptions import RequiredField


class StudentAsyncDatabase(AsyncBaseDatabase):
    async def get_student_subjects(self, user_id) -> list:
        async with self._async_session() as session:
            query = select(
                Users.first_name, Enrollments, Subjects.subject_name, Subjects.short_description,
                Subjects
            ).join(
                Enrollments, Users.user_id == Enrollments.user_id
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).where(Users.user_id == user_id).options(joinedload(Subjects.subject_theory))

            req = await session.execute(query)
            result = req.fetchall()
            return result

    async def get_student_subject_tasks_by_name(self, user_id, subject_name) -> list:
        query = select(
            SubjectTasks.task_name, SubjectTasks.subject_task_id, Users.user_id, Subjects.subject_id,
            Enrollments.enrollment_id
        ).join(
            Enrollments, Users.user_id == Enrollments.user_id
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            SubjectTasks, SubjectTasks.subject_id == Subjects.subject_id
        ).filter(
            Users.user_id == user_id, Subjects.subject_name == subject_name
        )
        async with self._async_session() as session:
            req = await session.execute(query)
            res = req.unique().scalars().all()
            return res

    async def add_teacher_subject_task(self, subject_id, task_name) -> bool:
        async with self._async_session() as session:
            if task_name is None:
                raise RequiredField('task_name')

            try:
                task = SubjectTasks(subject_id=subject_id, task_name=task_name)
                session.add(task)
                await session.commit()
                return True
            except Exception as ex:
                await session.rollback()
                print(ex)
                return False

    async def get_teacher_subject_tasks(self, user_id, subject_id) -> list[Type[SubjectTasks]]:
        async with self._async_session() as session:
            query = select(
                Users.user_id, Users.username, Subjects.subject_id, Subjects.subject_name, SubjectTasks.task_name,
                SubjectTasks.subject_task_id
            ).join(
                Subjects, Users.user_id == Subjects.user_id
            ).join(
                SubjectTasks, Subjects.subject_id == SubjectTasks.subject_id
            ).filter(
                Users.user_id == user_id, Subjects.subject_id == subject_id
            )
            req = await session.execute(query)
            result = req.fetchall()
            return result

    async def get_teacher_subjects(self, user_id) -> Type[Subjects]:
        async with self._async_session() as session:
            query = select(
                Subjects
            ).filter(Subjects.user_id == user_id)
            req = await session.execute(query)
            result = req.scalars().all()
            return result
