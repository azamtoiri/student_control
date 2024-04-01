# TODO: add with uid to id column on all functions
from typing import Type, Optional

from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker

from constants import Connection
from constants import UserDefaults
from database.models import (
    Base, Users, Subjects, Task, Enrollments, Grades, SubjectTasks, UserTasksFiles,
    UserTheme, SubjectTheory, TeacherInformation, TaskGrades
)
from utils.exceptions import (
    RequiredField, AlreadyRegistered, NotRegistered, DontHaveGrades, UserAlreadySubscribed,
    UserDontHaveGrade
)
from utils.jwt_hash import verify, hash_


class BaseDataBase:
    def __init__(self):
        engine = create_engine(url=Connection.DATABASE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()


class UserDatabase(BaseDataBase):
    def __init__(self) -> None:
        super().__init__()
        # self.create_default_user()

    # section user creating
    def create_default_user(self) -> None:
        """Creating default user"""
        username = UserDefaults.DEFAULT_USERNAME
        password = hash_(UserDefaults.DEFAULT_PASSWORD)
        if not self.filter_users(username=username):
            user = Users(username=username, password=password, email='admin@admin.com')
            self.insert_user(user)

    def filter_users(self, **value) -> list[Type[Users]]:
        """Filter users with added values"""
        return self.session.query(Users).filter_by(**value).all()

    def get_user_id(self, username) -> Type[Users]:
        """Get user id"""
        return self.session.query(Users).filter(Users.username == username).first()

    def get_user_by_id(self, user_id) -> Type[Users]:
        """Get user by id"""
        return self.session.query(Users).filter(Users.user_id == user_id).first()

    def insert_user(self, user: Users) -> None:
        """Registering user"""
        if user.username is None:
            raise RequiredField('username')

        elif user.password is None:
            raise RequiredField('password')

        elif self.filter_users(username=user.username):
            raise AlreadyRegistered('username')

        self.session.add(user)
        self.session.commit()

    def select_users(self) -> list[Type[Users]]:
        """Get all users"""
        return self.session.query(Users).all()

    def select_user_by_id(self, id: int) -> Optional[Users]:
        """Select user by id"""
        return self.session.query(Users).filter(Users.id == id).first()

    def verify_password(self, username: str, password: str) -> bool:
        """Verify password"""
        hashed_password = self.session.query(Users).filter_by(username=username).first()
        if not hashed_password:
            raise NotRegistered('username')
        try:
            if not verify(plain_password=password, hashed_password=hashed_password.password):
                raise NotRegistered('username')
        except ValueError as err:
            self.session.rollback()
            return False
        return True

    def get_user_image_url(self, user_id) -> str:
        query = self.session.query(Users).filter(Users.user_id == user_id).first()
        return query.user_image

    def set_new_user_image(self, user_id, image_url: str) -> bool:
        user = self.filter_users(user_id=user_id)
        try:
            user[0].user_image = image_url
            self.session.add(user[0])
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return False

    def register_user(
            self, first_name, last_name, middle_name, username,
            password, group: Optional[str] = None, course: Optional[str] = None,
            age: Optional[str] = None, email: Optional[str] = None
    ) -> Users:
        if first_name is None:
            raise RequiredField('first_name')
        if last_name is None:
            raise RequiredField('last_name')
        if middle_name is None:
            raise RequiredField('middle_name')

        if username is None:
            raise RequiredField('username')

        if password is None:
            raise RequiredField('password')

        if self.filter_users(username=username):
            raise AlreadyRegistered('username')

        user = Users(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            username=username,
            password=password,
            group=group,
            course=course,
            age=age,
            email=email
        )

        self.insert_user(user)

        return user

    def update_user(self, user_id, first_name, last_name, middle_name, group, course, age, email) -> bool:
        if first_name is None:
            raise RequiredField('Имя')
        if last_name is None:
            raise RequiredField('Фамилия')
        if middle_name is None:
            raise RequiredField('Отчество')

        user = self.get_user_by_id(user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.middle_name = middle_name
        user.group = group
        user.course = course
        user.age = age
        user.email = email
        self.session.add(user)
        self.session.commit()
        return True

    def login_user(
            self, username: Optional[str], password: Optional[str]
    ) -> Type[Users]:
        if username is None:
            raise RequiredField('username')

        if password is None:
            raise RequiredField('password')

        ver_pass = self.verify_password(username, password)
        users = self.filter_users(username=username)

        if not ver_pass:
            raise NotRegistered('Invalid username or password')
        else:
            return users[0]

    def is_staff(self, user_id: int) -> bool:
        return self.session.get(Users, user_id).is_staff

    def get_user_theme(self, user_id) -> Type[UserTheme]:
        return self.session.get(UserTheme, user_id)

    # region: Theme mode changing
    def add_theme_mode(self, user_id) -> bool:
        try:
            self.session.add(UserTheme(user_id=user_id))
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def set_theme_mode(self, user_id, theme_mode) -> bool:
        try:
            user_theme = self.get_user_theme(user_id)
            user_theme.theme = theme_mode
            self.session.add(user_theme)
            self.session.commit()

            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def get_theme_mode(self, user_id) -> str:
        try:
            return self.session.get(UserTheme, user_id).theme
        except AttributeError:
            self.add_theme_mode(user_id)
            # self.session.rollback()

    def set_seed_color(self, user_id, seed_color) -> bool:
        try:
            user_theme = self.get_user_theme(user_id)
            user_theme.seed_color = seed_color
            self.session.add(user_theme)
            self.session.commit()

            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def get_seed_color(self, user_id) -> str:
        return self.session.get(UserTheme, user_id).seed_color

    # endregion

    # region: Teacher info

    def get_teacher_info(self, user_id) -> Type[TeacherInformation]:
        return self.session.query(TeacherInformation).filter(TeacherInformation.user_id == user_id).first()

    def update_teacher_information(self, user_id, teacher_experience, teacher_description, is_done) -> bool:
        """Добавляем дополнительную информацию об учителе"""
        if teacher_experience is None:
            raise RequiredField('Опыт')
        if teacher_description is None:
            raise RequiredField('Описание')

        try:
            teacher_info = self.get_teacher_info(user_id)
            teacher_info.teacher_experience = teacher_experience
            teacher_info.teacher_description = teacher_description
            teacher_info.is_done = is_done
            self.session.add(teacher_info)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def create_teacher_information(self, user_id) -> bool:
        """Создаем в бд поле для заполнения информации об учителе"""
        try:
            if self.get_teacher_info(user_id) is not None:
                return True
            teacher_info = TeacherInformation(user_id=user_id)
            self.session.add(teacher_info)
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return False

    # endregion


class StudentDatabase(BaseDataBase):
    def get_course_by_id(self, _id) -> Type[Subjects]:
        return self.session.query(Subjects).filter(Subjects.subject_id == _id).first()

    def get_all_subjects(self) -> list[Type[Subjects]]:
        """Return all subjects use for subjects_view"""
        return self.session.query(Subjects).order_by(asc(Subjects.subject_name)).all()

    def get_subject(self, subject_id) -> Type[Subjects]:
        return self.session.query(Subjects).filter(Subjects.subject_id == subject_id).first()

    def get_student_subjects(self, username=None, user_id=None) -> list:
        """if not giv user_id getting from db"""
        if not user_id:
            user_id = UserDatabase().get_user_id(username).user_id
        user_subject = (
            self.session.query(
                Users.first_name, Enrollments, Subjects.subject_name, Subjects.short_description,
                Subjects
            ).join(
                Enrollments, Users.user_id == Enrollments.user_id
            ).join(
                Subjects, Subjects.subject_id == Enrollments.subject_id
            ).where(Users.user_id == user_id).all()
        )
        if len(user_subject) == 0:
            raise DontHaveGrades()
        return user_subject

    def get_student_subjects_and_completed_tasks(
            self, user_id=None, subject_task_id=None
    ) -> list[UserTasksFiles] or list:
        req = self.session.query(
            UserTasksFiles
        ).join(
            SubjectTasks
        ).filter(
            UserTasksFiles.user_id == user_id, UserTasksFiles.subject_task_id == subject_task_id
        ).all()
        return req

    def get_user_subjects(self, user_id):
        """Возвращает предмет пользователя который у него есть *(для учителя)*"""
        user = self.session.query(Users).filter_by(user_id=user_id).first()
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")

        # Получаем предметы (Subjects) для данного пользователя
        user_subjects = user.subjects

        return user_subjects

    def count_average_subject_grades(self, subject_name=None, user_id=None) -> int or str:
        """Возвращает среднюю оценку по предмету для пользователя"""
        avg_grade = (
            self.session.query(func.avg(Grades.grade_value))
            .join(Enrollments, Grades.enrollment_id == Enrollments.enrollment_id)
            .join(Users, Users.user_id == Enrollments.user_id)
            .join(Subjects, Subjects.subject_id == Enrollments.subject_id)
            .filter(Subjects.subject_name == subject_name, Users.user_id == user_id)
            .scalar()
        )

        if avg_grade is not None:
            return round(avg_grade)  # Округляем до целого числа
        else:
            return 'Нет оценок'

    def get_student_grade_for_exact_subject(self, username, sub_name) -> list:
        """Возвращает все оценки пользователя по определенному предмету"""
        values = self.session.query(
            Users.username, Subjects.subject_name, Grades.grade_value, Grades.grade_date, Enrollments.enrollment_date
        ).join(
            Users, Users.user_id == Enrollments.user_id,
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            Grades, Grades.enrollment_id == Enrollments.enrollment_id
        ).where(
            Users.username == username
        ).where(
            Subjects.subject_name == sub_name
        ).all()
        if not values:
            raise UserDontHaveGrade
        for value in values:
            yield value

    def get_student_grades(self, username=None, user_id=None) -> list:
        """
        Возвращает кортеж со всеми оценками определённого пользователя
        (username, subject_name, grade_value, grade_date, enrollment_date)
        """
        if not user_id:
            user_id = UserDatabase().get_user_id(username).user_id
        values = self.session.query(
            Users.username, Subjects.subject_name, Grades.grade_value, Grades.grade_date, Enrollments.enrollment_date
        ).join(
            Users, Users.user_id == Enrollments.user_id,
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            Grades, Grades.enrollment_id == Enrollments.enrollment_id
        ).filter(
            Users.user_id == user_id
        ).all()

        if len(values) < 1:
            raise DontHaveGrades()

        for value in values:
            yield value

    def get_student_task_grades_with_subject_name(self, user_id, subject_name) -> list[TaskGrades]:
        """Возвращает оценки студента по конкретному заданию."""

        # Запрос оценок для заданного пользователя и задания
        grades = (
            self.session.query(TaskGrades)
            .join(Enrollments)
            .join(Subjects)
            .join(SubjectTasks)
            .filter(
                Enrollments.user_id == user_id,
                Subjects.subject_name == subject_name
            )
            # .options(joinedload(TaskGrades.enrollment_grades))
            .all()
        )
        if len(grades) <= 0:
            raise UserDontHaveGrade

        return grades

    def get_student_tasks_grades_v2(self, user_id) -> list[Type[TaskGrades]] | list:
        try:
            return self.session.query(TaskGrades).filter(TaskGrades.user_id == user_id).all()
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return []

    def count_average_tasks_subject_grade(self, subject_name, user_id) -> int or str:
        avg_grade = (
            self.session.query(func.avg(TaskGrades.grade_value))
            .join(Enrollments, Enrollments.enrollment_id == TaskGrades.enrollment_id)
            .join(Subjects, Subjects.subject_id == Enrollments.subject_id)
            .filter(Subjects.subject_name == subject_name, Enrollments.user_id == user_id)
            .scalar()
        )

        if avg_grade is not None:
            return round(avg_grade)  # Округляем до целого числа
        else:
            return 'Нет оценок'

    def check_student_subscribe(self, user_id, subject_id) -> bool:
        """Проверяет подписку студента на определенный предмет"""
        subscription = self.session.query(Enrollments).filter(
            Enrollments.user_id == user_id,
            Enrollments.subject_id == subject_id
        ).first()

        return bool(subscription)

    def subscribe_student_to_subject(self, user_id, subject_id) -> bool:
        try:
            enrollment = Enrollments(user_id=user_id, subject_id=subject_id)
            if self.check_student_subscribe(user_id, subject_id):
                raise UserAlreadySubscribed
            self.session.add(enrollment)
            self.session.commit()
        except UserAlreadySubscribed:
            return False
        except Exception as ex:
            self.session.rollback()
            return False

    def unsubscribe_student_from_subject(self, user_id, subject_id) -> bool:
        """Удаляет записанный курс вместе с его оценка в таблице grades"""
        enrollment = self.session.query(Enrollments).where(
            Enrollments.user_id == user_id
        ).where(
            Enrollments.subject_id == subject_id
        ).first()
        try:
            self.session.delete(enrollment)
            self.session.commit()
        except Exception:
            self.session.rollback()
            return True

    def filter_subjects_by_name(self, subject_name) -> list[Type[Subjects]]:
        """Для поиска предмета по имени"""
        return self.session.query(Subjects).filter(Subjects.subject_name.ilike(f'%{subject_name}%')).all()

    def get_student_subject_tasks(self, user_id) -> list:
        """Get all subject_tasks of user"""
        res = self.session.query(
            SubjectTasks.subject_task_id, SubjectTasks.task_name, Users.user_id, Subjects.subject_name,
            Enrollments.enrollment_id
        ).join(
            Enrollments, Users.user_id == Enrollments.user_id
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            SubjectTasks, SubjectTasks.subject_id == Subjects.subject_id
        ).where(
            Users.user_id == user_id
        ).all()
        return res

    def get_all_grades(self, user_id) -> int:
        """Return quantity of user final grades"""
        values = self.session.query(
            Subjects.subject_name, Grades.grade_value, Grades.grade_date, Enrollments.enrollment_date
        ).join(
            Users, Users.user_id == Enrollments.user_id,
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            Grades, Grades.enrollment_id == Enrollments.enrollment_id
        ).where(
            Users.user_id == user_id
        ).all()

        return len(values)

    def quantity_of_subjects(self, user_id) -> int:
        return len(self.get_student_subjects(user_id=user_id))

    def get_student_subject_tasks_by_name(self, user_id, subject_name) -> list:
        res = self.session.query(
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
        ).all()
        for r in res:
            yield r

    # region: subject_task_file
    def get_status_of_task_by_user_id(self, user_id, subject_task_id, enrollment_id):
        """Gets status of the subject_task"""
        if not self.check_task_file_exist(user_id, subject_task_id):
            self.add_subject_task_file(user_id, subject_task_id, enrollment_id)

        status = self.session.query(
            UserTasksFiles.completed
        ).join(
            SubjectTasks
        ).filter(
            UserTasksFiles.user_id == user_id,
            SubjectTasks.subject_task_id == subject_task_id
        ).first()

        return status[0] if status is not None else None

    def get_completed_task_status(self, user_id, subject_task_id) -> Type[UserTasksFiles]:
        return self.session.query(UserTasksFiles).filter(
            UserTasksFiles.user_id == user_id,
            UserTasksFiles.subject_task_id == subject_task_id
        ).first()

    def delete_task_file(self, task_file) -> bool:
        try:
            self.session.delete(task_file)
            self.session.commit()

            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def check_task_file_exist(self, user_id, subject_task_id) -> bool:
        """Проверяет есть ли такая запись в таблице"""
        # Используем метод query.exists() для проверки существования записи в запросе
        exists = self.session.query(
            self.session.query(UserTasksFiles)
            .join(SubjectTasks)
            .filter(UserTasksFiles.user_id == user_id, SubjectTasks.subject_task_id == subject_task_id)
            .exists()
        ).scalar()

        return exists

    def add_subject_task_file(self, user_id, subject_task_id, enrollment_id, file_name) -> bool:
        try:
            # checking status exist before adding
            sub_status = UserTasksFiles(user_id=user_id, subject_task_id=subject_task_id, enrollment_id=enrollment_id,
                                        task_file=file_name)
            self.session.add(sub_status)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def change_task_file(self, user_id, subject_task_id, file_name: bool) -> bool:
        try:
            completed_task_status = self.get_completed_task_status(user_id, subject_task_id)
            completed_task_status.task_file = file_name
            self.session.add(completed_task_status)
            self.session.commit()

            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    # endregion

    # region: Teacher subjects
    def get_teacher_subjects(self, user_id) -> list[Type[Subjects]]:
        return self.session.query(Subjects).filter(Subjects.user_id == user_id).all()

    def update_subject(
            self, subject_id, subject_name, subject_short_description, subject_description,
    ) -> bool:
        if subject_name is None:
            raise RequiredField('Имя предмета')
        if subject_short_description is None:
            raise RequiredField('Краткое описание предмета')
        if subject_description is None:
            raise RequiredField('Описание предмета')

        try:
            subject = self.get_subject(subject_id)
            subject.subject_name = subject_name
            subject.short_description = subject_short_description
            subject.description = subject_description
            self.session.add(subject)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def create_subject(self, user_id, subject_name, subject_short_description, subject_description) -> bool:
        if subject_name is None:
            raise RequiredField('Имя предмета')
        if subject_short_description is None:
            raise RequiredField('Краткое описание предмета')
        if subject_description is None:
            raise RequiredField('Описание предмета')

        try:
            subject = Subjects(
                user_id=user_id,
                subject_name=subject_name,
                short_description=subject_short_description,
                description=subject_description
            )
            self.session.add(subject)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()  # Откатываем транзакцию в случае ошибки
            return False

    def delete_subject(self, subject_id) -> bool:
        try:
            subject = self.get_subject(subject_id)
            self.session.delete(subject)
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return False

    # endregion

    # region: Teacher tasks

    def get_teacher_subject_tasks(self, user_id, subject_id) -> list[Type[SubjectTasks]]:
        return self.session.query(
            Users.user_id, Users.username, Subjects.subject_id, Subjects.subject_name, SubjectTasks.task_name,
            SubjectTasks.subject_task_id
        ).join(
            Subjects, Users.user_id == Subjects.user_id
        ).join(
            SubjectTasks, Subjects.subject_id == SubjectTasks.subject_id
        ).filter(
            Users.user_id == user_id, Subjects.subject_id == subject_id
        ).all()

    def add_teacher_subject_task(self, subject_id, task_name) -> bool:
        if task_name is None:
            raise RequiredField('task_name')

        try:
            task = SubjectTasks(subject_id=subject_id, task_name=task_name)
            self.session.add(task)
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return False

    def get_task_by_id(self, task_id) -> Type[SubjectTasks]:
        return self.session.get_one(SubjectTasks, task_id)

    def delete_teacher_subject_task(self, subject_task_id) -> bool:
        try:
            task = self.get_task_by_id(subject_task_id)
            self.session.delete(task)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    # endregion


class TheoryDatabase(BaseDataBase):
    def get_theory(self, subject_id) -> Type[SubjectTheory]:
        """
        Возвращает теорию по предмету
        subject_id = theory_id
        """
        return self.session.get(SubjectTheory, subject_id)


class TaskDatabase(BaseDataBase):
    def get_all_user_tasks(self, user_id) -> list[Type[Task]]:
        return self.session.query(Task).filter(Task.user_id == user_id).all()

    def add_task(self, task: Task) -> Task | bool:
        try:
            self.session.add(task)
            self.session.commit()

            return task
        except Exception as ex:
            self.session.rollback()
            return False

    def get_task_by_id(self, _id) -> Type[Task]:
        return self.session.query(Task).filter(Task.task_id == _id).first()

    def delete_task(self, task_id) -> bool:
        task = self.get_task_by_id(task_id)
        self.session.delete(task)
        self.session.commit()
        return True

    def clear_all_tasks(self, user_id) -> bool:
        tasks = self.get_all_user_tasks(user_id)
        for task in tasks:
            self.delete_task(task)
        return True

    def set_status(self, task_id, status) -> bool:
        try:
            task = self.get_task_by_id(task_id)
            task.completed = status
            self.session.add(task)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def updated_task(self, task_id, new_task_value) -> bool:
        try:
            task = self.get_task_by_id(task_id)
            task.task_name = new_task_value
            self.session.add(task)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return False

    def get_count_of_tasks(self, user_id):
        return len(self.session.query(Task).filter(Task.user_id == user_id).where(Task.completed == False).all())


if __name__ == '__main__':
    a = StudentDatabase()
