import pytest

from database.models import Users, SubjectTasks, Subjects
from test_teacher_operations import test_create_subject
from utils import db_session


@pytest.mark.usefixtures("db_session")
def test_create_teacher(db_session):
    # Создание учителя для теста
    user = Users(
        last_name="Тестовый",
        first_name="Учитель",
        middle_name="Тестович",
        age=30,
        group="1",
        course=2,
        email="test@example.com",
        username="tester",
        password="tester",
        is_staff=True
    )
    db_session.add(user)
    db_session.commit()

    # Проверка, что пользователь был успешно создан
    queried_user = db_session.query(Users).filter_by(username='tester').first()
    assert queried_user is not None
    assert queried_user.email == 'test@example.com'
    assert queried_user.is_staff is True


@pytest.mark.usefixtures("db_session")
def test_create_subject_task(db_session):
    test_create_subject(db_session)
    queried_subject = db_session.query(Subjects).filter_by(subject_name='Математика').first()
    # Создаем задание для предмета
    subject_task = SubjectTasks(
        task_name="Решить уравнения",
        completed=False,
        subject_id=queried_subject.subject_id
    )
    db_session.add(subject_task)
    db_session.commit()

    # Проверяем, что задание для предмета было создано
    assert subject_task.subject_id == queried_subject.subject_id
    assert subject_task.task_name == "Решить уравнения"
    assert subject_task.completed is False
