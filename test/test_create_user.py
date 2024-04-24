import pytest

from database.models import Users
from utils import db_session


@pytest.mark.usefixtures("db_session")
def test_create_user(db_session):
    # Создание пользователя для теста
    user_data = {
        'last_name': 'Doe',
        'first_name': 'John',
        'email': 'john.doe@example.com',
        'username': 'tester',
        'password': 'password123'
    }
    user = Users(**user_data)
    db_session.add(user)
    db_session.commit()

    # Проверка, что пользователь был успешно создан
    queried_user = db_session.query(Users).filter_by(username='tester').first()
    assert queried_user is not None
    assert queried_user.email == 'john.doe@example.com'
