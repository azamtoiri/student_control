import flet as ft
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.database import StudentDatabase, StudentAsyncDatabase
from database.database import async_engine
from user_controls.student_subject_tasks_card import create_student_subject_tasks_card
from utils.exceptions import DontHaveGrades
from utils.lazy_db import LazyDatabase

async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True
)


async def TasksView(page: ft.Page) -> ft.Column:
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    if len(page.views) > 1:
        page.views.pop()

    db = LazyDatabase(StudentDatabase)
    async_db = StudentAsyncDatabase()

    content = ft.Column()

    dont_have_tasks = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        controls=[ft.Text('Нет заданий', size=20, text_align=ft.TextAlign.CENTER, color=ft.colors.SURFACE_TINT)]
    )

    # region: FilePicker
    file_piker = ft.FilePicker()
    page.overlay.append(file_piker)
    page.update()

    # endregion

    try:
        subjects = await async_db.get_student_subjects(user_id=USER_ID)
        for subject in subjects:
            content.controls.append(
                await create_student_subject_tasks_card(
                    USER_ID, subject[2],
                    subject[4].subject_id,
                    page=page,
                    file_picker=file_piker,
                    theory_url=subject[4].subject_theory.theory_data if subject[4].subject_theory else None
                )
            )
    except DontHaveGrades as error:
        dont_have_tasks.visible = True
        page.update()
    except Exception as err:
        print(err)

    return dont_have_tasks


async def create_text_field(label):
    return ft.Column([ft.TextField(label=label)])


async def main(page: ft.Page):
    text_field = await create_text_field('skdfj')
    tt = await TasksView(page)
    page.add(tt)
    page.update()


if __name__ == '__main__':
    ft.app(main)
