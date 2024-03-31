import flet as ft
from flet_route import Params, Basket

from database.database import TheoryDatabase
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes

# theory_db: LazyDatabase = LazyDatabase(TheoryDatabase)
theory_db = TheoryDatabase()


def SubjectTheoryView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    SUBJECT_THEORY_ID = params.get('id')
    # data = theory_db.database.get_theory(SUBJECT_THEORY_ID)
    data = theory_db.get_theory(SUBJECT_THEORY_ID)

    content = ft.Column()
    if data is not None:
        content.controls.append(ft.Text(f'{data.theory_title}'))
        content.controls.append(ft.Text(f'{data.theory_data}'))
    else:
        content.controls.append(ft.Text(f'Пока теории нет'))

    return ft.View(
        route=StudentRoutes.SUBJECT_THEORY_URL,
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.colors.SURFACE_VARIANT,
        controls=[
            content
        ]
    )
