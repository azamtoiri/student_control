from typing import Type, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from constants import UserDefaults
from database.models import Base, Users, Subjects, Task, Enrollments, Grades
from utils.exceptions import RequiredField, AlreadyRegistered, NotRegistered, DontHaveGrades
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
        self.create_default_user()

    # section user creating
    def create_default_user(self) -> None:
        """Creating default user"""
        username = UserDefaults.DEFAULT_USERNAME
        password = hash_(UserDefaults.DEFAULT_PASSWORD)
        if not self.filter_users(username=username):
            user = Users(username=username, password=password)
            self.insert_user(user)

    def filter_users(self, **value) -> list[Type[Users]]:
        """Filter users with added values"""
        return self.session.query(Users).filter_by(**value).all()

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
            verify(plain_password=password, hashed_password=hashed_password.password)
        except ValueError as err:
            return False
        return True

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


class StudentDatabase(BaseDataBase):
    def get_all_courses(self) -> list[Type[Subjects]]:
        return self.session.query(Subjects).all()

    def get_course_by_id(self, _id) -> Type[Subjects]:
        return self.session.query(Subjects).filter(Subjects.subject_id == _id).first()

    def get_all_subjects(self) -> list[Type[Subjects]]:
        return self.session.query(Subjects).all()

    def get_student_subjects(self, username) -> list:
        user_subject = (
            self.session.query(Users.first_name, Enrollments, Subjects.subject_name)
            .join(Enrollments, Users.user_id == Enrollments.user_id)
            .join(Subjects, Subjects.subject_id == Enrollments.subject_id).where(Users.username == username).all()
        )
        if len(user_subject) == 0:
            raise DontHaveGrades
        return user_subject

    def get_student_subjects_by_name(self, username, sub_name) -> list:
        """Возвращает конкретный записанный курс у пользователя"""
        return self.session.query(Users.username, Subjects.subject_name, Enrollments.subject_id).join(
            Users, Users.user_id == Enrollments.user_id,
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).where(
            Users.username == username
        ).where(
            Subjects.subject_name == sub_name
        ).all()

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
        for value in values:
            yield value

    def get_student_grades(self, username) -> list:
        """
        Возвращает кортеж со всеми оценками определённого пользователя
        (username, subject_name, grade_value, grade_date, enrollment_date)
        """
        value = self.session.query(
            Users.username, Subjects.subject_name, Grades.grade_value, Grades.grade_date, Enrollments.enrollment_date
        ).join(
            Users, Users.user_id == Enrollments.user_id,
        ).join(
            Subjects, Subjects.subject_id == Enrollments.subject_id
        ).join(
            Grades, Grades.enrollment_id == Enrollments.enrollment_id
        ).where(
            Users.username == username
        ).all()

        for i in range(len(value)):
            # print(value[i])
            yield value[i]


class TaskDatabase(BaseDataBase):
    def get_all_user_tasks(self, user_id) -> list[Type[Task]]:
        return self.session.query(Task).filter(Task.user_id == user_id).all()

    def add_task(self, task: Task) -> Task | bool:
        try:
            self.session.add(task)
            self.session.commit()

            return task
        except Exception as ex:
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
            return False


if __name__ == '__main__':
    a = StudentDatabase()
