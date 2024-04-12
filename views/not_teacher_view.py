import flet as ft
from flet_route import Params, Basket

from utils.routes_url import BaseRoutes


async def NotTeacherView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route=BaseRoutes.NOT_TEACHER_URL,
        controls=[
            ft.Text(f"{page.route} Page not found error 404", size=40, color=ft.colors.GREY),
            ft.ElevatedButton('Назад', on_click=lambda _: page.go(page.views[-2].route))]
    )
