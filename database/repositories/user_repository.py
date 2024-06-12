import asyncio
from typing import Type, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from constants import UserDefaults
from database.engine.base_async import AsyncBaseDatabase
from database.models import (
    Users, UserTheme, TeacherInformation, Enrollments
)
from utils.exceptions import (
    RequiredField, AlreadyRegistered, NotRegistered
)
from utils.jwt_hash import verify, hash_


class UserRepository(AsyncBaseDatabase):
    def __init__(self):
        super().__init__()
        # self.create_default_user()

    async def create_default_user(self) -> None:
        """Creating default user"""
        try:
            async with self.session_scope() as session:
                username = UserDefaults.DEFAULT_USERNAME
                password = hash_(UserDefaults.DEFAULT_PASSWORD)
                if not await self.filter_users(username=username):
                    user = Users(username=username, password=password, email='admin@admin.com')
                    await self.insert_user(user)
        except Exception as err:
            print(err)

    async def filter_users(self, **value) -> list[Type[Users]]:
        """Filter users with added values"""
        try:
            async with self.session_scope() as session:
                query = select(Users).filter_by(**value)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as err:
            print(err)

    async def insert_user(self, user: Users):
        """Registering user"""
        try:
            async with self.session_scope() as session:
                if user.username is None:
                    raise RequiredField('username')

                elif user.password is None:
                    raise RequiredField('password')

                elif await self.filter_users(username=user.username):
                    raise AlreadyRegistered('username')

                session.add(user)
                await session.commit()
        except Exception as err:
            print(err)

    async def get_user_by_id(self, user_id) -> Users:
        """
        Get user by id
        :return Users
        """
        async with self.session_scope() as session:
            query = select(Users).filter(Users.user_id == user_id).options(joinedload(Users.user_theme)).options()
            response = await session.execute(query)
            result = response.scalars().first()
            return result

    async def verify_password(self, username: str, password: str) -> bool:
        """Verify password"""
        async with self.session_scope() as session:
            hashed_password = await self.filter_users(username=username)
            if not hashed_password:
                raise NotRegistered('username')
            try:
                if not verify(plain_password=password, hashed_password=hashed_password[0].password):
                    raise NotRegistered('username')
            except ValueError as err:
                await session.rollback()
                return False
            return True

    async def get_user_image_url(self, user_id) -> str:
        try:
            async with self.session_scope() as session:
                query = select(Users).filter(Users.user_id == user_id)
                result = await session.execute(query)
            return result.scalars().first().user_image
        except Exception as err:
            print(err)

    async def set_new_user_image(self, user_id, image_url: str) -> bool:
        async with self.session_scope() as session:
            user = await self.filter_users(user_id=user_id)
            try:
                user[0].user_image = image_url
                session.add(user[0])
                await session.commit()
                return True
            except Exception as ex:
                await session.rollback()
                print(ex)
                return False

    async def register_user(
            self, first_name, last_name, middle_name, username,
            password, group: Optional[str] = None, course: Optional[str] = None,
            age: Optional[str] = None, email: Optional[str] = None
    ) -> Users:
        if first_name is None:
            raise RequiredField('first_name')
        if last_name is None:
            raise RequiredField('middle_name')

        if username is None:
            raise RequiredField('username')

        if password is None:
            raise RequiredField('password')

        if await self.filter_users(username=username):
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

        await self.insert_user(user)

        return user

    async def update_user(self, user_id, first_name, last_name, middle_name, group, course, age, email) -> bool:
        async with self.session_scope() as session:
            if first_name is None:
                raise RequiredField('Имя')
            if last_name is None:
                raise RequiredField('Фамилия')
            if middle_name is None:
                raise RequiredField('Отчество')

            user = await self.get_user_by_id(user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.middle_name = middle_name
            user.group = group
            user.course = course
            user.age = int(age)
            user.email = email
            session.add(user)
            await session.commit()
            return True

    async def login_user(
            self, username: Optional[str], password: Optional[str]
    ) -> Type[Users]:
        if username is None:
            raise RequiredField('username')

        if password is None:
            raise RequiredField('password')

        ver_pass = await self.verify_password(username, password)
        users = await self.filter_users(username=username)

        if not ver_pass:
            raise NotRegistered('Invalid username or password')
        else:
            return users[0]

    async def is_staff(self, user_id) -> bool:
        async with self.session_scope() as session:
            user: Users = await self.get_user_by_id(user_id)
            return user.is_staff

    # region: Teacher info
    async def get_teacher_info(self, user_id) -> Type[TeacherInformation]:
        """Get teacher information by teacher id"""
        async with self.session_scope() as session:
            query = select(TeacherInformation).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().first()

    async def update_teacher_information(self, user_id, teacher_experience, teacher_description, is_done) -> bool:
        """Добавляем дополнительную информацию об учителе"""
        if teacher_experience is None:
            raise RequiredField('Опыт')
        if teacher_description is None:
            raise RequiredField('Описание')

        async with self.session_scope() as session:
            try:
                teacher_info = await self.get_teacher_info(user_id)
                teacher_info.teacher_experience = int(teacher_experience)
                teacher_info.teacher_description = teacher_description
                teacher_info.is_done = is_done
                session.add(teacher_info)
                await session.commit()
                return True
            except Exception as ex:
                print(ex)
                await session.rollback()
                return False

    async def create_teacher_information(self, user_id) -> bool:
        """Создаем в бд поле для заполнения информации об учителе"""
        async with self.session_scope() as session:
            try:
                if await self.get_teacher_info(user_id) is not None:
                    return True
                teacher_info = TeacherInformation(user_id=user_id)
                session.add(teacher_info)
                await session.commit()
                return True
            except Exception as ex:
                await session.rollback()
                print(ex)
                return False

    # endregion

    # region: Theme mode changing

    async def get_theme_settings(self, user_id) -> Type[UserTheme]:
        async with self.session_scope() as session:
            user_theme = await session.get(UserTheme, user_id)
            return user_theme

    async def get_user_theme(self, user_id) -> Type[UserTheme]:
        async with self.session_scope() as session:
            result = await session.get(UserTheme, user_id)
            return result

    async def add_theme_mode(self, user_id) -> bool:
        async with self.session_scope() as session:
            session.add(UserTheme(user_id=user_id))
            await session.commit()
        return True

    async def get_theme_mode(self, user_id) -> str:
        async with self.session_scope() as session:
            try:
                result = await session.get(UserTheme, user_id)
                return result.theme
            except AttributeError:
                await self.add_theme_mode(user_id)

    async def set_seed_color(self, user_id, seed_color) -> bool:
        async with self.session_scope() as session:
            try:
                user_theme = await self.get_user_theme(user_id)
                user_theme.seed_color = seed_color
                session.add(user_theme)
                await session.commit()

                return True
            except Exception as ex:
                print(ex)
                await session.rollback()
                return False

    async def get_seed_color(self, user_id) -> str:
        async with self.session_scope() as session:
            result = await session.get(UserTheme, user_id)
            return result.seed_color

    # endregion


async def main():
    db = UserRepository()
    async with db.session_scope() as session:
        query = select(Users)
        response = await session.execute(query)
        result: list[Users] = response.scalars().all()
        user_id = result[0].user_id

    user = await db.get_user_by_id(user_id)
    print(user.user_theme)


if __name__ == '__main__':
    asyncio.run(main())
