import uuid

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func, expression

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Таблица пользователей'}

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment='User id column')
    last_name = Column(String, comment='Фамилия')
    first_name = Column(String, comment='Имя')
    middle_name = Column(String, comment='Отчество')
    age = Column(Integer)
    group = Column(String)
    course = Column(Integer, comment='Курс обучения')
    email = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, comment='уникальное Имя пользователя')
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, server_default=expression.false(), default=False,
                      comment='является ли пользователь частью персонала (преподаватель)')
    is_superuser = Column(Boolean, server_default=expression.false(), default=False,
                          comment='является ли пользователь суперпользователем')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                        comment='Дата создания пользователя')
    user_image = Column(String, server_default='default_user_image.png', default='default_user_image.png',
                        comment='Изображение пользователя')

    enrollments = relationship('Enrollments', backref='users', cascade='all, delete-orphan, delete')
    subjects = relationship('Subjects', back_populates='users', cascade='all, delete-orphan')
    user_theme = relationship(
        'UserTheme', back_populates='users', cascade='all, delete-orphan', uselist=False
    )
    teacher_info = relationship(
        'TeacherInformation', back_populates='user', cascade='all, delete-orphan', uselist=False
    )


class TeacherInformation(Base):
    __tablename__ = 'teacher_information'
    __table_args__ = {
        "comment": "Дополнительная информация о преподавателе"
    }

    teacher_information_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                    comment='идентификатор информации')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='id пользователя')
    teacher_experience = Column(Integer, nullable=True, comment='опыт преподавателя')
    teacher_description = Column(String, nullable=True, comment='Информация о преподавателе')
    is_done = Column(Boolean, nullable=False, default=False, server_default=expression.false())

    user = relationship('Users', back_populates='teacher_info')


class UserTheme(Base):
    __tablename__ = 'user_theme'
    __table_args__ = {'comment': 'Цветовая схема пользователя (тема). Уникальная для каждого пользователя'}

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True,
                     comment='Идентификатор пользователя')
    theme = Column(String, nullable=False, server_default='light', default='light',
                   comment='Тема пользователя (светлая/темная)')
    seed_color = Column(String, nullable=False, server_default='green', default='green',
                        comment='Цвет цветовой схемы приложения')

    users = relationship('Users', back_populates='user_theme')


class SubjectTheory(Base):
    __tablename__ = 'subject_theory'
    __table_args__ = {'comment': 'Теория для предмета. У каждого предмета может быть только одна теория в виде файла'}

    theory_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'), primary_key=True,
                       comment='Идентификатор теории')
    theory_data = Column(String, nullable=True, comment='Данные теории (файл, текст, ссылка)')

    subject = relationship('Subjects', back_populates='subject_theory', uselist=False)


class SubjectTasks(Base):
    __tablename__ = 'subject_tasks'
    __table_args__ = {'comment': 'Задания для предмета. У каждого предмета может быть несколько заданий'}

    subject_task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                             comment='Идентификатор задания')
    task_name = Column(String, nullable=False, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'),
                        comment='Идентификатор предмета')

    task_files = relationship('UserTasksFiles', backref='subject_task', cascade='all, delete-orphan', uselist=False)
    subject = relationship('Subjects', back_populates='subject_tasks')


class Subjects(Base):
    __tablename__ = 'subjects'
    __table_args__ = {
        'comment': 'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов'
    }

    subject_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                        comment='Идентификатор предмета')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Идентификатор пользователя')
    subject_name = Column(String, nullable=False, comment='Название предмета')
    short_description = Column(String, nullable=False, comment='Краткое описание предмета')
    description = Column(String, nullable=False, comment='Полное описание предмета')
    subject_image = Column(String, nullable=False, default='subject_image.png', server_default='subject_image.png',
                           comment='Изображения для предмета')

    enrollments = relationship('Enrollments', backref='subject', cascade='all, delete-orphan')
    subject_tasks = relationship('SubjectTasks', back_populates='subject', cascade='all, delete-orphan')
    subject_theory = relationship(
        'SubjectTheory', uselist=False, back_populates='subject', cascade='all, delete-orphan'
    )

    users = relationship('Users', back_populates='subjects')


class Grades(Base):
    __tablename__ = 'grades'
    __table_args__ = {'comment': 'Итоговая оценка студентов по предметам'}

    grade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                      comment='Идентификатор оценки')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=False, comment='Идентификатор записи о подписке')
    grade_value = Column(Integer, nullable=False, comment='Сама оценка')
    grade_date = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                        comment='Дата выставления оценки')


class TaskGrades(Base):
    __tablename__ = 'task_grades'
    __table_args__ = {'comment': 'Оценки за задания по предметам'}

    task_grade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                           comment='Идентификатор оценки за задание')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=True,
                           comment='Идентификатор записи о подписке')
    subject_task_id = Column(UUID(as_uuid=True), ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'),
                             nullable=False, comment='Идентификатор задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Идентификатор пользователя, который выполнил задание')
    grade_value = Column(Integer, nullable=False, comment='Оценка за задание')
    grade_date = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=func.now(),
        comment='Дата постановки оценки'
    )

    # Добавим связи
    enrollment = relationship('Enrollments', back_populates='task_grades_list', foreign_keys=[enrollment_id])
    subject_task = relationship('SubjectTasks', backref='task_grades')
    users = relationship('Users', backref='task_grades')


class Enrollments(Base):
    __tablename__ = 'enrollments'
    __table_args__ = {'comment': 'Записи о подписках пользователей на предметы'}

    enrollment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                           comment='Идентификатор записи о подписке')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     comment='Пользователь, подписавшийся на предмет')
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subject_id', ondelete='CASCADE'), nullable=False,
                        comment='Предмет, на который подписался пользователь. Сам предмет')
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(),
                             comment='Дата подписки')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус завершения предмета')

    task_files = relationship('UserTasksFiles', backref='enrollments', cascade='all, delete-orphan')
    task_grades_list = relationship('TaskGrades', back_populates='enrollment', cascade='all, delete-orphan',
                                    foreign_keys=[TaskGrades.enrollment_id])


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {
        'comment': 'Todo list. Задания пользователей которые они должны выполнить (цели). '
    }

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
                     comment='Идентификатор задания')
    task_name = Column(String, nullable=False, comment='Название задания')
    completed = Column(Boolean, server_default=expression.false(), default=False, comment='Статус задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False,
                     comment='Пользователь которому принадлежит задание')


class UserTasksFiles(Base):
    __tablename__ = 'user_task_files'
    __table_args__ = {
        'comment': 'Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов'
    }

    subject_task_id = Column(UUID(as_uuid=True), ForeignKey('subject_tasks.subject_task_id', ondelete='CASCADE'),
                             nullable=False, primary_key=True, comment='Идентификатор задания')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                     primary_key=True, comment='пользователь')
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'),
                           nullable=False, comment='предмет на который записан пользователй')
    task_file = Column(String, nullable=False, comment='файл прикрепленный к заданию')
    completed = Column(Boolean, nullable=False, default=True, server_default=expression.true(),
                       comment='Отправил ли ученик задание')

    user = relationship('Users', backref='user_task_files')
