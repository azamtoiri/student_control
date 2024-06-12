import asyncio
from typing import Type
from uuid import UUID

from sqlalchemy import select, asc, func
from sqlalchemy.orm import joinedload

from database.engine.base_async import AsyncBaseDatabase
from database.models import Users, Enrollments, Subjects, SubjectTasks, SubjectTheory, Grades
from utils.exceptions import RequiredField, DontHaveGrades


class StudentRepository(AsyncBaseDatabase):
    async def get_subject(self, subject_id) -> Type[Subjects]:
        """
        Get subject by subject id
        :param subject_id:
        :return:
        """
        async with self.session_scope() as session:
            query = select(Subjects).filter(Subjects.subject_id == subject_id)
            req = await session.execute(query)
            res = req.scalars().first()
            return res

    async def get_student_subjects(self, user_id) -> list[tuple[str, Enrollments, str, str, Subjects]]:
        """
        Get students subjects
        :param user_id: UUID
        :return: list[tuple(username, object[Enrollments], Subject name, subject description object[Subjects]
        """
        async with self.session_scope() as session:
            query = select(
                Users.first_name, Enrollments, Subjects.subject_name, Subjects.short_description,
                Subjects
            ).join(
                Enrollments, Users.user_id == Enrollments.user_id
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).where(Users.user_id == user_id).options(
                joinedload(Subjects.subject_theory).subqueryload(SubjectTheory.subject)
            ).options(
                joinedload(Subjects.enrollments)
            )

            req = await session.execute(query)
            result = req.unique().all()
            return result

    async def get_student_subject_tasks_by_name(self, user_id, subject_name) -> list[
        tuple[str, UUID, UUID, UUID, UUID, SubjectTasks]]:
        """
        Получить задания по предметам учащихся по имени предмета
        :param user_id: UUID
        :param subject_name: Subject name
        :return: list[tuple]
        One example return:
        ('Изучить законы Ньютона', - task_name
         UUID('d1044fb5-2915-4230-9676-4512eed0f063'), - task_id
          UUID('221286db-470a-4475-ad18-0683c2a10ce0'), - User_id
           UUID('6db41504-0c90-4a6a-b13f-32c435b38acb'), - subject_id
            UUID('132e6ea3-ceb4-4128-968e-571b4c521c39'), - enrollment_id
             <database.models.subjects.subject_tasks.SubjectTasks object at 0x000001877F62BF90> - joined SubjectTasks taskfiles
             )
        """
        query = select(
            SubjectTasks.task_name, SubjectTasks.subject_task_id, Users.user_id, Subjects.subject_id,
            Enrollments.enrollment_id, SubjectTasks
        ).join(
            Enrollments, Users.user_id == Enrollments.user_id
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            SubjectTasks, SubjectTasks.subject_id == Subjects.subject_id
        ).filter(
            Users.user_id == user_id, Subjects.subject_name == subject_name
        ).options(joinedload(SubjectTasks.task_files))
        async with self.session_scope() as session:
            req = await session.execute(query)
            res = req.fetchall()
            return res

    async def get_all_subjects(self) -> list[Type[Subjects]]:
        async with self.session_scope() as session:
            query = select(Subjects).order_by(asc(Subjects.subject_name))
            req = await session.execute(query)
            res = req.scalars().all()
            return res

    async def count_average_subject_grades(self, subject_name=None, user_id=None) -> int or str:
        async with self.session_scope() as session:
            query = select(
                func.avg(Grades.grade_value)
            ).join(
                Enrollments, Grades.enrollment_id == Enrollments.enrollment_id
            ).join(
                Users, Users.user_id == Enrollments.user_id
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).filter(Subjects.subject_name == subject_name, Users.user_id == user_id)

            req = await session.execute(query)
            res = req.scalars().first()
            if res is not None:
                return round(res)  # Округляем до целого числа
            else:
                return 'Нет оценок'

    async def get_student_grades(self, username=None, user_id=None) -> list:
        """
        Возвращает кортеж со всеми оценками определённого пользователя
        (username, subject_name, grade_value, grade_date, enrollment_date)
        :param username:
        :param user_id:
        :return:
        """
        async with self.session_scope() as session:
            query = select(
                Users.username, Subjects.subject_name, Grades.grade_value, Grades.grade_date,
                Enrollments.enrollment_date
            ).join(
                Users, Users.user_id == Enrollments.user_id,
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).join(
                Grades, Grades.enrollment_id == Enrollments.enrollment_id
            ).filter(
                Users.user_id == user_id
            )
            req = await session.execute(query)
            res = req.scalars().all()
            if len(res) < 1:
                raise DontHaveGrades()
            return res

    async def get_all_grades(self, user_id) -> int:
        async with self.session_scope() as session:
            query = select(
                Subjects.subject_name, Grades.grade_value, Grades.grade_date, Enrollments.enrollment_date
            ).join(
                Users, Users.user_id == Enrollments.user_id,
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).join(
                Grades, Grades.enrollment_id == Enrollments.enrollment_id
            ).where(
                Users.user_id == user_id
            )
            req = await session.execute(query)
            res = req.fetchall()
            return len(res)

    async def count_average_tasks_subject_grade(self, subject_name, user_id) -> int:
        async with self.session_scope() as session:
            query = select(
                func.avg(Grades.grade_value)
            ).join(
                Enrollments, Grades.enrollment_id == Enrollments.enrollment_id
            ).join(
                Users, Users.user_id == Enrollments.user_id
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).filter(Subjects.subject_name == subject_name, Users.user_id == user_id)

            req = await session.execute(query)
            res = req.scalars().first()
            if res is not None:
                return round(res)
            else:
                return 'Нет оценок'

    # region: Teacher
    async def add_teacher_subject_task(self, subject_id, task_name) -> bool:
        """
        Добавить задание на предмет учителя
        :param subject_id:
        :param task_name:
        :return:
        """
        async with self.session_scope() as session:
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
        """
        Получить задания учителя по предмету
        :param user_id:
        :param subject_id:
        :return:
        """
        async with self.session_scope() as session:
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

    async def get_teacher_subjects(self, user_id) -> Type[list[Subjects]]:
        async with self.session_scope() as session:
            query = select(
                Subjects
            ).filter(Subjects.user_id == user_id)
            req = await session.execute(query)
            result = req.fetchall()
            return result

    # endregion


async def main():
    from database.database import StudentDatabase
    st_db = StudentDatabase()
    res = st_db.count_average_subject_grades('Математика', '5866d8e6-f202-47bc-a389-efb976894aff')
    print(res)
    db = StudentRepository()
    students = await db.count_average_subject_grades('Математика', '5866d8e6-f202-47bc-a389-efb976894aff')
    subjects = await db.get_all_grades('221286db-470a-4475-ad18-0683c2a10ce0')
    print(subjects)


if __name__ == '__main__':
    asyncio.run(main())
