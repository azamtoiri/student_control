import pytest

from database.models import Enrollments, Subjects, Users
from test_create_user import test_create_user
from utils import db_session


@pytest.mark.usefixtures("db_session")
def test_create_subject(db_session):
    test_create_user(db_session)
    queried_user = db_session.query(Users).filter_by(username='tester').first()
    # Создание предмета для теста
    subject_data = {
        'subject_name': 'Математика',
        'short_description': 'Изучения чисел, величин, пространства',
        'description': 'Математика – это наука о числах, количестве и пространстве.',
        'user_id': queried_user.user_id
    }
    subject = Subjects(**subject_data)
    db_session.add(subject)
    db_session.commit()

    # Проверка, что предмет был успешно создан
    queried_subject = db_session.query(Subjects).filter_by(subject_name='Математика').first()
    assert queried_subject is not None
    assert queried_subject.short_description == 'Изучения чисел, величин, пространства'


@pytest.mark.usefixtures("db_session")
def test_create_enrollment(db_session):
    test_create_subject(db_session)
    # Создание записи о подписке для теста
    user = db_session.query(Users).filter_by(username='tester').first()
    subject = db_session.query(Subjects).filter_by(subject_name='Математика').first()
    enrollment_data = {
        'user_id': user.user_id,
        'subject_id': subject.subject_id
    }
    enrollment = Enrollments(**enrollment_data)
    db_session.add(enrollment)
    db_session.commit()

    # Проверка, что запись о подписке была успешно создана
    queried_enrollment = db_session.query(Enrollments).filter_by(user_id=user.user_id).first()
    assert queried_enrollment is not None
    assert queried_enrollment.subject_id == subject.subject_id
