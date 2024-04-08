import asyncio

import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.bg_animation import Thing
from utils.routes_url import BaseRoutes


def IndexView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.session.clear()
    logo_image = ft.Image(src=LOGO_PATH)
    logo_image.width = 100
    logo_image.height = 100
    logo_image.expand = True
    page.padding = 0

    logo_text = ft.Text(
        value="FoxHub",
        weight=ft.FontWeight.BOLD,
        color=ft.colors.with_opacity(1, "White"),
        size=30,
        expand=1,
        text_align="center"
    )

    welcome_text = ft.Text(
        value='Добро пожаловать',
        size=34,
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
        expand=1
    )

    login_button = ft.ElevatedButton(
        text='Войти',
        icon=ft.icons.LOGIN,
        expand=True,
        on_click=lambda _: page.go(BaseRoutes.LOGIN_URL)  # handler
    )

    register_button = ft.ElevatedButton(
        text='Регистрация',
        icon=ft.icons.APP_REGISTRATION,
        expand=True,
        on_click=lambda _: page.go(BaseRoutes.REGISTER_URL)  # handler
    )

    content = ft.Column()
    content.width = 400
    content.alignment = ft.MainAxisAlignment.CENTER
    content.controls.append(ft.Row([logo_image]))
    content.controls.append(ft.Row([logo_text]))
    content.controls.append(ft.Row([welcome_text]))
    content.controls.append(ft.Row([login_button]))
    content.controls.append(ft.Row([register_button]))

    container = ft.Container()
    container.bgcolor = ft.colors.TRANSPARENT
    container.border_radius = 8
    container.content = content
    container.width = 450
    container.height = 650
    container.padding = ft.padding.all(40)
    container.border = ft.border.all(1, ft.colors.TRANSPARENT)

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route=BaseRoutes.INDEX_URL,
        controls=[container]
    )
