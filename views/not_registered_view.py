import flet as ft
from flet_route import Params, Basket

from utils.routes_url import BaseRoutes


def NotRegistered(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    async def go_back(e: ft.ControlEvent):
        await page.go_async(BaseRoutes.LOGIN_URL)

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route=BaseRoutes.NOT_REGISTERED_URL,
        controls=[ft.Text('Вы не вошли в аккаунт', size=40, color=ft.colors.GREY),
                  ft.ElevatedButton('На страницу входа', on_click=go_back)]
    )
