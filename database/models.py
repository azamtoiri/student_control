from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func, expression

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Таблица пользователей'}

    user_id = Column(Integer, primary_key=True, comment='User id column')  # id
    last_name = Column(String, comment='Фамилия')  # fam
    first_name = Column(String, comment='Имя')  # imya
    middle_name = Column(String, comment='Отчество')  # отчество
    age = Column(Integer)  # let
    group = Column(String)  # группа
    course = Column(Integer, comment='Курс обучения')  # курс
    email = Column(String, nullable=False)  # email
    username = Column(String, unique=True, nullable=False, comment='уникальное Имя пользователя')  # username for login
    password = Column(String, nullable=False)  # password for login
    is_staff = Column(
        Boolean, server_default=expression.false(), default=False,
        comment='является ли пользователь частью персонала (преподаватель)'
    )
    is_superuser = Column(
        Boolean, server_default=expression.false(), default=False,
        comment='является ли пользователь суперпользователем'
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now(),
        comment='Дата создания пользователя'
    )
    user_image = Column(
        String, server_default='default_user_image.png', default='default_user_image.png',
        comment='Изображение пользователя'
    )

    enrollments = relationship('Enrollments', backref='users', cascade='all, delete-orphan, delete')
    subjects = relationship('Subjects', backref='users', cascade='all, delete-orphan')
    user_theme = relationship('UserTheme', back_populates='users', cascade='all, delete-orphan', uselist=False)


class UserTheme(Base):
    __tablename__ = 'user_theme'
    __table_args__ = {'comment': 'Цветовая схема пользователя (тема). Уникальная для каждого пользователя'}

    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True, comment='Идентификатор пользователя'
    )
    theme = Column(
        String, nullable=False, server_default='light', default='light', comment='Тема пользователя (светлая/темная)'
    )
    seed_color = Column(
        String, nullable=False, server_default='green', default='green', comment='Цвет цветовой схемы приложения'
    )

    users = relationship('Users', back_populates='user_theme')


class SubjectTheory(Base):
    __tablename__ = 'subject_theory'
    __table_args__ = {'comment': 'Теория для предмета. У каждого предмета может быть только одна теория'}

    theory_id = Column(
        Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'), primary_key=True,
        comment='Идентификатор теории'
    )
    theory_title = Column(String, unique=True, nullable=False, comment='Заголовок теории')
    theory_data = Column(String, nullable=False, comment='Данные теории (файл, текст, ссылка)')

    subject = relationship('Subjects', back_populates='subject_theory')


class SubjectTasks(Base):
    __tablename__ = 'subject_tasks'
    __table_args__ = {'comment': 'Задания для предмета. У каждого предмета может быть несколько заданий'}

    subject_task_id = Column(
        Integer, primary_key=True, unique=True, nullable=False,
        comment='Идентификатор задания'
    )
    task_name = Column(String, nullable=False, unique=True, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    subject_id = Column(
        Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'),
        comment='Идентификатор предмета'
    )


class Subjects(Base):
    __tablename__ = 'subjects'
    __table_args__ = {
        'comment': 'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов'
    }

    subject_id = Column(Integer, primary_key=True, nullable=False, comment='Идентификатор предмета')
    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False, comment='Идентификатор пользователя'
    )
    subject_name = Column(String, nullable=False, comment='Название предмета')
    short_description = Column(String, nullable=False, comment='Краткое описание предмета')
    description = Column(String, nullable=False, comment='Полное описание предмета')

    enrollments = relationship('Enrollments', backref='subject', cascade='all, delete-orphan')
    subject_tasks = relationship('SubjectTasks', backref='subject', cascade='all, delete-orphan')
    subject_theory = relationship(
        'SubjectTheory', uselist=False, back_populates='subject', cascade='all, delete-orphan'
    )


class Grades(Base):
    __tablename__ = 'grades'
    __table_args__ = {'comment': 'Оценки студентов по предметам'}

    grade_id = Column(Integer, primary_key=True, nullable=False, comment='Идентификатор оценки')
    enrollment_id = Column(
        Integer, ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'), nullable=False,
        comment='Идентификатор записи о подписке'
    )
    grade_value = Column(Integer, nullable=False, comment='Сама оценка')
    grade_date = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now(), comment='Дата выставления оценки'
    )


# todo: Date time now for creating
class Enrollments(Base):
    __tablename__ = 'enrollments'
    __table_args__ = {'comment': 'Записи о подписках пользователей на предметы'}

    enrollment_id = Column(Integer, primary_key=True, nullable=False, comment='Идентификатор записи о подписке')
    user_id = Column(
        Integer, ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False, comment='Пользователь, подписавшийся на предмет'
    )
    subject_id = Column(
        Integer, ForeignKey('subjects.subject_id', ondelete='CASCADE'), nullable=False,
        comment='Предмет, на который подписался пользователь. Сам предмет'
    )
    enrollment_date = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now(),
        comment='Дата подписки'
    )
    completed = Column(
        Boolean, server_default=expression.false(), default=False, comment='Статус завершения предмета'
    )

    task_files = relationship('UserTasksFiles', backref='enrollments', cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {
        'comment': 'Todo list. Задания пользователей которые они должны выполнить (цели). '
    }

    task_id = Column(Integer, primary_key=True, nullable=False, comment='Идентификатор задания')
    task_name = Column(String, nullable=False, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    user_id = Column(
        Integer, ForeignKey('users.user_id'), nullable=False, comment='Пользователь которому принадлежит задание'
    )


class UserTasksFiles(Base):
    __tablename__ = 'user_task_files'
    __table_args__ = {
        'comment': 'Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов'
    }

    subject_task_id = Column(
        Integer, ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'), nullable=False,
        primary_key=True, comment='Идентификатор задания'
    )
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'), nullable=False)
    task_file = Column(String, nullable=False)
    completed = Column(
        Boolean, nullable=False, default=True, server_default=expression.true(), comment='Отправил ли ученик задание'
    )

    subject_task = relationship('SubjectTasks', backref='user_task_files', cascade='all')
    user = relationship('Users', backref='user_task_files', cascade='all')
