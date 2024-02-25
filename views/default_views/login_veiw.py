import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.custom_input_field import CustomInputField


def LoginView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    logo_icon = ft.Image(src=LOGO_PATH)
    logo_icon.width = 100
    logo_icon.height = 100
    logo_icon.expand = True

    logo_text = ft.Text()
    logo_text.value = 'FoxHub'
    logo_text.weight = ft.FontWeight.BOLD
    logo_text.text_align = ft.TextAlign.CENTER
    logo_text.color = ft.colors.BLACK
    logo_text.size = 30
    logo_text.expand = True

    title = ft.Text()
    title.value = "Вход"
    title.theme_style = ft.TextThemeStyle.TITLE_MEDIUM
    title.text_align = ft.TextAlign.CENTER
    title.color = ft.colors.BLACK
    title.size = 20
    title.width = ft.FontWeight.BOLD
    title.expand = True

    username_field = CustomInputField(False, 'Имя пользователя')
    password_field = CustomInputField(True, 'Пароль')
    # endregion

    # region: Buttons
    login_button = ft.ElevatedButton()
    login_button.text = "Войти"
    login_button.icon = ft.icons.LOGIN
    login_button.width = 400
    login_button.height = 45
    login_button.expand = True
    login_button.on_click = lambda _: page.go('/student/main')  # handler

    create_account_button = ft.Container()
    create_account_button.content = ft.Text(
        "Регистрация", size=15, color=ft.colors.with_opacity(0.50, ft.colors.BLUE))
    create_account_button.alignment = ft.alignment.center
    create_account_button.width = 150
    create_account_button.height = 45
    create_account_button.on_click = lambda _: page.go('/register')
    # endregion

    # region: Texts
    text_dont_not_registered = ft.Text()
    text_dont_not_registered.value = "Еще нет аккаунта?"
    text_dont_not_registered.size = 15
    text_dont_not_registered.color = ft.colors.with_opacity(0.50, ft.colors.BLACK)
    # endregion

    content = ft.Column()
    content.spacing = 20
    content.width = 400
    content.alignment = ft.MainAxisAlignment.CENTER
    content.controls.append(ft.Row([logo_icon]))
    content.controls.append(ft.Row([logo_text]))
    content.controls.append(ft.Row([title]))
    content.controls.append(username_field)
    content.controls.append(password_field)
    content.controls.append(ft.Row([login_button]))
    #
    content.controls.append(ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[text_dont_not_registered, create_account_button]))

    container = ft.Container()
    container.bgcolor = ft.colors.WHITE
    container.border_radius = 8
    container.content = content
    container.width = 450
    container.height = 650
    container.padding = ft.padding.all(40)
    container.border = ft.border.all(1, ft.colors.TRANSPARENT)

    return ft.View(
        route='/register',
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[container]
    )
