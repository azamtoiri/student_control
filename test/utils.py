import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from database.models import Base


@pytest.fixture
def db_session():
    engine = create_engine(Connection.TEST_DATABASE)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session_no_delete():
    engine = create_engine(Connection.TEST_DATABASE)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
