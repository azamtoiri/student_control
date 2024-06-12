import asyncio
from typing import Type

from sqlalchemy import select

from database.engine.base_async import AsyncBaseDatabase
from database.models import (
    UserTheme, Users
)


class UserThemeRepository(AsyncBaseDatabase):
    async def get_user_theme(self, user_id) -> Type[UserTheme]:
        async with self.session_scope() as session:
            query = select(UserTheme).filter(UserTheme.user_id == user_id)
            response = await session.execute(query)
            return response.scalars().first()

    async def add_theme_mode(self, user_id) -> bool:
        async with self.session_scope() as session:
            session.add(UserTheme(user_id=user_id))
            await session.commit()
        return True

    async def set_theme_mode(self, user_id, theme_mode) -> bool:
        async with self.session_scope as session:
            user_theme = await self.get_user_theme(user_id)
            user_theme.theme = theme_mode
            session.add(user_theme)
            await session.commit()
            return True

    async def get_theme_mode(self, user_id) -> str:
        """
        Get theme mode
        :param user_id:
        :return: str: user theme mode light\blaack
        """
        try:
            async with self.session_scope() as session:
                query = select(UserTheme).filter(UserTheme.user_id == user_id)
                result = await session.execute(query)
                response = result.scalars().first()
                return response.theme
        except AttributeError:
            await self.add_theme_mode(user_id)

    async def set_seed_color(self, user_id, seed_color) -> bool:
        try:
            async with self.session_scope() as session:
                user_theme = await self.get_user_theme(user_id)
                user_theme.seed_color = seed_color
                session.add(user_theme)
                await session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    async def get_seed_color(self, user_id) -> str:
        """Get seed color for ColorScheme"""
        async with self.session_scope() as session:
            query = select(UserTheme).filter(UserTheme.user_id == user_id)
            response = await session.execute(query)
            result = response.scalars().first()
            return result.seed_color


# testing
async def main():
    db = UserThemeRepository()
    async with db.session_scope() as session:
        query = select(Users)
        response = await session.execute(query)
        result = response.scalars().all()
        user_id = result[0].user_id
    theme = await db.get_seed_color(user_id)
    print(theme)


if __name__ == '__main__':
    asyncio.run(main())
