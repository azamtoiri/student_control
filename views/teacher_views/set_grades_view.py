import flet as ft
from flet_route import Basket, Params

from utils.routes_url import TeacherRoutes


def SetGradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.GRADES_URL,
    )