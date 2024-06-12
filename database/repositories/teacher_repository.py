from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import aliased

from database.engine.base_async import AsyncBaseDatabase
from database.models import Users, Enrollments, Subjects
from utils.exceptions import DontHaveGrades


class TeacherRepository(AsyncBaseDatabase):

    async def get_teacher_students(self, user_id) -> list[Type[Users]]:
        """Возвращает студентов препод. Которые записались на его курс только одних"""
        try:
            user1 = aliased(Users)

            # Выполняем запрос для получения студентов
            stmt = (
                select(
                    Users.user_id.label('student_id'),
                    Users.first_name.label('student_first_name'),
                    Users.last_name.label('student_last_name')
                )
                .join(Enrollments, Users.user_id == Enrollments.user_id)
                .join(Subjects, Enrollments.subject_id == Subjects.subject_id)
                .join(user1, Subjects.user_id == user1.user_id)
                .filter(user1.is_staff == True)
                .filter(user1.user_id == user_id)
                .distinct()
            )

            async with self._async_session() as session:
                result = await session.execute(stmt)
                students = result.fetchall()

            if len(students) <= 0:
                raise DontHaveGrades()

            return students
        except Exception as ex:
            print(ex)
            await session.rollback()

    async def get_teacher_students_with_subjects(self, user_id) -> list[Type[Users]]:
        try:
            user1 = aliased(Users)

            stmt = (
                select(
                    Users.user_id.label('student_id'),
                    Users.first_name.label('student_first_name'),
                    Users.last_name.label('student_last_name'),
                    Subjects.subject_name,
                    Subjects.subject_id
                )
                .join(Enrollments, Users.user_id == Enrollments.user_id)
                .join(Subjects, Enrollments.subject_id == Subjects.subject_id)
                .join(user1, Subjects.user_id == user1.user_id)
                .filter(user1.is_staff == True)
                .filter(user1.user_id == user_id)
            )

            async with self._async_session() as session:
                result = await session.execute(stmt)
                students_with_subjects = result.fetchall()

            if len(students_with_subjects) <= 0:
                raise DontHaveGrades

            return students_with_subjects
        except Exception as ex:
            print(ex)

    async def get_teacher_students_subjects_with_filter(self, user_id, subject_name) -> list[Type[Users]]:
        try:
            user1 = aliased(Users)

            # Выполняем запрос для получения студентов
            stmt = (
                select(Users.user_id, Users.first_name, Users.last_name, Subjects.subject_name,
                       Subjects.subject_id)
                .join(Enrollments, Users.user_id == Enrollments.user_id)
                .join(Subjects, Enrollments.subject_id == Subjects.subject_id)
                .join(user1, Subjects.user_id == user1.user_id)
                .filter(user1.is_staff == True)
                .distinct()
                .filter(user1.user_id == user_id, Subjects.subject_name.ilike(f'%{subject_name}%'))
            )

            async with self._async_session() as session:
                result = await session.execute(stmt)
                students = result.fetchall()

            if len(students) <= 0:
                raise DontHaveGrades

            return students
        except Exception as ex:
            print(ex)

    async def get_teacher_students_with_filter(self, user_id, last_name) -> list[Type[Users]]:
        user1 = aliased(Users)
        async with self._async_session() as session:
            # Выполняем запрос для получения студентов
            query = (
                select(
                    Users.user_id,
                    Users.first_name,
                    Users.last_name,
                    Subjects.subject_name,
                    Subjects.subject_id
                )
                .join(Enrollments, Users.user_id == Enrollments.user_id)
                .join(Subjects, Enrollments.subject_id == Subjects.subject_id)
                .join(user1, Subjects.user_id == user1.user_id)
                .filter(user1.is_staff == True)
                .distinct()
                .filter(user1.user_id == user_id, Users.last_name.ilike(f'%{last_name}%'))
            )
            result = await session.execute(query)
            students = result.fetchall()

            if len(students) <= 0:
                raise DontHaveGrades

            return students
