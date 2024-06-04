from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from database.model_base import Base


class BaseDataBase:
    def __init__(self):
        engine = create_engine(url=Connection.DATABASE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()
