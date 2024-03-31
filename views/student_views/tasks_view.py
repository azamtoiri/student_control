import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from user_controls.student_subject_tasks_card import StudentSubjectTasksCard
from utils.exceptions import DontHaveGrades
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes


def TasksView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    if len(page.views) > 1:
        page.views.pop()

    db = LazyDatabase(StudentDatabase)

    content = ft.Column()

    dont_have_tasks = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        controls=[ft.Text('Нет заданий', size=20, text_align=ft.TextAlign.CENTER, color=ft.colors.SURFACE_TINT)]
    )

    try:
        subjects = db.database.get_student_subjects(user_id=USER_ID)

        for subject in subjects:
            content.controls.append(StudentSubjectTasksCard(USER_ID, subject[2], subject[4].subject_id, page=page))
    except DontHaveGrades as error:
        dont_have_tasks.visible = True
        page.update()

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=StudentRoutes.TASKS_URL,
        controls=[
            content,
            dont_have_tasks
        ]
        # controls=content
    )
