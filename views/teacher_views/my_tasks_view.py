import flet as ft
from flet_route import Basket, Params

from database.database import StudentDatabase as TeacherDatabase
from user_controls.student_subject_tasks_card import StudentSubjectTasksCard
from user_controls.teacher_add_task_card import TeacherAddTaskCard
from utils.routes_url import TeacherRoutes

db = TeacherDatabase()


def MyTasksView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # Constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    # Remove the last view from the views list
    if len(page.views) > 2:
        page.views.pop()

    content = ft.Column()

    try:
        subjects = db.get_teacher_subjects(user_id=USER_ID)

        for subject in subjects:
            content.controls.append(TeacherAddTaskCard(USER_ID, subject.subject_name, subject.subject_id, page=page))
    except Exception as error:
        print(error)
        page.update()

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.TASKS_URL,
        controls=[
            content,
        ]
    )
