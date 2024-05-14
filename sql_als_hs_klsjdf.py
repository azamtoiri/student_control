import asyncio
import uuid
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import joinedload

from constants import Connection
from database.models import Users, Enrollments, Subjects, SubjectTasks
from utils.exceptions import RequiredField

engine = create_async_engine(
    url=Connection.ASYNC_DATABASE_URL, echo=True
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_user(session: AsyncSession, user_id) -> Type[Users] | None:
    query = select(Users).filter(Users.user_id == user_id).options(joinedload(Users.user_theme))
    req = await session.execute(query)
    result = req.unique().scalars().first()
    return result


async def get_student_subjects(session: AsyncSession, user_id) -> list:
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


async def get_student_subject_tasks_by_name(session: AsyncSession, user_id, subject_name) -> list:
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
    req = await session.execute(query)
    res = req.unique().scalars().all()
    return res


async def get_teacher_subject_tasks(session: AsyncSession, user_id, subject_id) -> list[Type[SubjectTasks]]:
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
    print(result)


async def add_teacher_subject_task(session, subject_id, task_name) -> bool:
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


async def get_teacher_subjects(session: AsyncSession, user_id) -> Type[Subjects]:
    result = await session.get(Subjects, user_id)
    return result


async def main():
    async with async_session() as session:
        # result = await get_student_subject_tasks_by_name(
        #     session, uuid.UUID('d4f65688-690f-4217-9394-4d6aa54a6aa2'),
        #     'Естествознание'
        # )
        res = await get_teacher_subject_tasks(
            session, uuid.UUID('7831a720-646e-4f5a-8114-cfdb4e0cac02'),
            uuid.UUID('01479a81-cb0e-40a1-a16e-e4b65fbb85b0')
        )


if __name__ == '__main__':
    asyncio.run(main())
