import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH


def IndexView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    route = "/welcome"

    logo_image = ft.Image(src=LOGO_PATH)
    logo_image.width = 100
    logo_image.height = 100
    logo_image.expand = True

    logo_text = ft.Text()
    logo_text.value = "FoxHub"
    logo_text.width = ft.FontWeight.BOLD
    logo_text.text_align = ft.TextAlign.CENTER
    logo_text.color = ft.colors.with_opacity(1, "White")
    logo_text.size = 30
    logo_text.expand = True

    welcome_text = ft.Text()
    welcome_text.value = "Добро пожаловать"
    welcome_text.size = 34
    welcome_text.width = ft.FontWeight.W_500
    welcome_text.text_align = ft.TextAlign.CENTER
    welcome_text.color = ft.colors.with_opacity(1, "White")
    welcome_text.expand = True

    login_button = ft.ElevatedButton()
    login_button.text = 'Войти'
    login_button.icon = ft.icons.LOGIN
    login_button.expand = True

    register_button = ft.ElevatedButton()
    register_button.text = 'Регистрация'
    register_button.icon = ft.icons.APP_REGISTRATION
    register_button.expand = True

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
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route='/',
        controls=[container]
    )
