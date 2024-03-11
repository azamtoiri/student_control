import flet as ft
from flet_route import Params, Basket

from utils.routes_url import BaseRoutes


def NotRegistered(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route=BaseRoutes.NOT_REGISTERED_URL,
        controls=[ft.Text('Вы не вошли в аккаунт', size=40, color=ft.colors.GREY),
                  ft.ElevatedButton('На страницу входа', on_click=lambda _: page.go(BaseRoutes.LOGIN_URL))]
    )