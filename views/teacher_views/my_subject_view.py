import flet as ft
from flet_route import Basket, Params

from utils.routes_url import TeacherRoutes


def MySubjectView(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    return ft.View(
        route=TeacherRoutes.SUBJECT_URL,
    )