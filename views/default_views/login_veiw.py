import asyncio

import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from database.database import UserDatabase
from user_controls.custom_input_field import CustomInputField
from utils.exceptions import RequiredField, NotRegistered

user_db = UserDatabase()


def LoginView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    async def display_login_form_error(field: str, message: str) -> None:
        fields = {'username': username_field, 'password': password_field}
        if field in fields.keys():
            # fields[field].input_box_content.error_text = message
            asyncio.run(fields[field].set_fail(message))
            await page.update_async()

    # region: Functions
    async def login_click(e: ft.ControlEvent) -> None:
        username = str(username_field.input_box_content.value).strip() if len(
            username_field.input_box_content.value) else None
        password = str(password_field.input_box_content.value).strip() if len(
            password_field.input_box_content.value) else None

        try:
            user = user_db.login_user(username, password)
            e.page.session.set("is_auth", True)
            e.page.session.set("username", username)
            e.page.session.set("user_id", user.user_id)

            if user_db.is_staff(user.user_id):
                e.page.session.set("is_staff", True)
                await e.page.go_async('/teacher/main')
            else:
                e.page.route = '/student/main'
                await page.update_async()

        except RequiredField as error:
            await display_login_form_error(error.field, str(error))
        except NotRegistered as error:
            await display_login_form_error('username', str(error))

        # page.route = '/student/main'
        # page.update_async()

    async def register_click(e: ft.ControlEvent) -> None:
        await e.page.go_async('/register')

    # endregion

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
    username_field.input_box_content.on_submit = login_click
    password_field = CustomInputField(True, 'Пароль')
    password_field.input_box_content.on_submit = login_click
    # endregion

    # region: Buttons
    login_button = ft.ElevatedButton()
    login_button.text = "Войти"
    login_button.icon = ft.icons.LOGIN
    login_button.width = 400
    login_button.height = 45
    login_button.expand = True
    login_button.on_click = login_click

    create_account_button = ft.Container()
    create_account_button.content = ft.Text(
        "Регистрация", size=15, color=ft.colors.with_opacity(0.50, ft.colors.BLUE))
    create_account_button.alignment = ft.alignment.center
    create_account_button.width = 150
    create_account_button.height = 45
    create_account_button.on_click = register_click
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

    container = ft.Container(shadow=ft.BoxShadow(
        color='grey', offset=ft.Offset(1, 2), blur_radius=10,
    ))
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
