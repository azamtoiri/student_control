# CREATE SUPERUSER
# UPDATE USER IS_STAFF TO TRUE
import argparse
import asyncio

from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from database.engine.base_async import AsyncBaseDatabase
from database.models import Users

async_engine = AsyncBaseDatabase()
async_session = async_sessionmaker(async_engine.async_engine, class_=AsyncSession, expire_on_commit=False)


async def update_user(username, **kwargs):
    try:
        async with async_session() as session:
            async with session.begin():
                stmt = update(Users).where(Users.username == username).values(**kwargs)
                await session.execute(stmt)
                await session.commit()
                print(f"Пользователю {username} был успешно обновлен")
    except Exception as err:
        print(err)
        print("Не смогли дать права пользователю")


async def main(username, is_staff=None, is_superuser=None):
    try:
        update_data = {}
        if is_staff is not None:
            update_data['is_staff'] = is_staff
        if is_superuser is not None:
            update_data['is_superuser'] = is_superuser
        await update_user(username, **update_data)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update user information')
    parser.add_argument('-u', '--username', type=str, required=True, help='User username')
    parser.add_argument('--is-staff', action='store_true', help='Set user as staff')
    parser.add_argument('--is-superuser', action='store_true', help='Set user as superuser')

    args = parser.parse_args()

    username = args.username

    asyncio.run(main(username, is_staff=args.is_staff, is_superuser=args.is_superuser))
