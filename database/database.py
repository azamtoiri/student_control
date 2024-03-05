from typing import Type, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from database.models import Base, Users
from utils.exceptions import RequiredField, AlreadyRegistered, NotRegistered
from utils.jwt_hash import verify, hash_
from constants import UserDefaults


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
