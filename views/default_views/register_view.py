import asyncio
import time

import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from database.database import UserDatabase
from user_controls.banners import SuccessBanner
from user_controls.custom_input_field import CustomInputField
from user_controls.input_filter import TextOnlyInputFilterRu
from utils.exceptions import RequiredField, PasswordDontMatching, AlreadyRegistered, NotRegistered
from utils.jwt_hash import hash_

user_db = UserDatabase()


def RegisterView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # region: Functions
    def display_register_form_error(field: str, message: str) -> None:
        password_field2 = password2_field

        fields = {
            'first_name': first_name_field,
            'last_name': last_name_field,
            'middle_name': middle_name_field,
            'group': group_field,
            "course": course_field,
            "age": age_field,
            "email": email_field,
            'username': username_field,
            'password': password_field,
            'password2': password_field2
        }
        if field in fields.keys():
            # fields[field].input_box_content.error_text = message
            asyncio.run(fields[field].set_fail(message))
            page.update()

    def display_success_banner(message: str) -> None:
        banner = SuccessBanner(page, message)
        page.show_banner(banner)
        page.update()

    def hide_banner() -> None:
        if page.banner is not None:
            page.banner.open = False
            page.update()

    def login_click(e: ft.ControlEvent) -> None:
        e.page.route = '/login'
        e.page.update()

    def register_click(e: ft.Container) -> None:
        try:

            # region: Form fields
            first_name = str(first_name_field.input_box_content.value).strip() if len(
                first_name_field.input_box_content.value) else None

            last_name = str(last_name_field.input_box_content.value).strip() if len(
                last_name_field.input_box_content.value) else None

            middle_name = str(middle_name_field.input_box_content.value).strip() if len(
                middle_name_field.input_box_content.value) else None

            group = str(group_field.input_box_content.value).strip() if len(
                group_field.input_box_content.value) else None

            course = str(course_field.input_box_content.value).strip() if len(
                course_field.input_box_content.value) else None

            age = str(age_field.input_box_content.value).strip() if len(age_field.input_box_content.value) else None

            email = str(email_field.input_box_content.value).strip() if len(
                email_field.input_box_content.value) else None

            username = str(username_field.input_box_content.value).strip() if len(
                username_field.input_box_content.value) else None

            password = str(password_field.input_box_content.value).strip() if len(
                password_field.input_box_content.value) else None

            password2 = str(password2_field.input_box_content.value).strip() if len(
                password2_field.input_box_content.value) else None
            # endregion

            if password2 is None and username and password is None:
                raise RequiredField('password')
            elif password2 is None and username:
                raise RequiredField('password2')
            elif password != password2:
                raise PasswordDontMatching('password2')
            elif password and password2:
                # hashing password
                password = hash_(password2)

            user_db.register_user(
                first_name=first_name, last_name=last_name, middle_name=middle_name,
                username=username, password=password, group=group, course=course, age=age, email=email
            )

            page.route = '/login'
            page.update()
            display_success_banner('Вы были успешно зарегистрированы')
            time.sleep(2)
            hide_banner()
        except RequiredField as error:
            display_register_form_error(error.field, str(error))

        except NotRegistered as error:
            display_register_form_error('username', str(error))

        except AlreadyRegistered as error:
            # display_warning_banner(str(error))
            display_register_form_error('username', str(error))
        except PasswordDontMatching as error:
            display_register_form_error(error.field, str(error))
        except Exception as error:
            print(error)
            # display_warning_banner(str(error))

    # endregion

    # region: Header
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
    title.value = "Регистрация"
    title.theme_style = ft.TextThemeStyle.TITLE_MEDIUM
    title.text_align = ft.TextAlign.CENTER
    title.color = ft.colors.BLACK
    title.size = 20
    title.width = ft.FontWeight.BOLD
    title.expand = True

    # endregion

    class MixedCustomInputField(CustomInputField):  # for rule DRY
        def __init__(self, password: bool, title: str):
            super().__init__(password, title)
            self.obj.width = 300

    # region: InputFields
    first_name_field = MixedCustomInputField(False, "Фамилия *")  # Фамилия
    last_name_field = MixedCustomInputField(False, "Имя *")  # Имя
    middle_name_field = MixedCustomInputField(False, "Отчество *")  # Отчество
    group_field = MixedCustomInputField(False, "Группа")  # Группа
    course_field = MixedCustomInputField(False, "Курс")  # Звание
    age_field = MixedCustomInputField(False, "Возраст")  # Возраст
    email_field = MixedCustomInputField(False, "Email")  # Email
    username_field = MixedCustomInputField(False, "Имя пользователя - Логин *")  # Имя пользователя - Логин
    password_field = MixedCustomInputField(True, "Пароль *")  # Пароль
    password2_field = MixedCustomInputField(True, "Введите пароль еще раз *")  # Пароль

    # Adding filters on fields
    first_name_field.input_box_content.input_filter = TextOnlyInputFilterRu()
    last_name_field.input_box_content.input_filter = TextOnlyInputFilterRu()
    middle_name_field.input_box_content.input_filter = TextOnlyInputFilterRu()
    course_field.input_box_content.input_filter = ft.NumbersOnlyInputFilter()
    age_field.input_box_content.input_filter = ft.NumbersOnlyInputFilter()
    # endregion

    # region: Buttons
    register_button = ft.ElevatedButton()
    register_button.text = 'Создать аккаунт'
    register_button.width = 300
    register_button.height = 45
    register_button.icon = ft.icons.KEY
    register_button.on_click = lambda e: register_click(e)

    login_button = ft.Container()
    login_button.alignment = ft.alignment.center
    login_button.content = ft.Text(
        value='Войти', size=15, color=ft.colors.with_opacity(0.5, ft.colors.BLUE)
    )
    login_button.on_click = lambda e: login_click(e)
    # endregion

    # region: Some text
    already_hav_account = ft.Text("У  вас уже есть аккаунт")
    already_hav_account.size = 15
    already_hav_account.color = ft.colors.with_opacity(0.5, ft.colors.BLACK)
    # endregion

    # content = ft.Column()
    content = ft.ResponsiveRow(
        spacing=5
    )
    content.alignment = ft.MainAxisAlignment.CENTER
    content.controls.append(ft.Row([logo_icon]))
    content.controls.append(ft.Row([logo_text]))
    content.controls.append(ft.Row([title]))
    content.controls.append(ft.Column(col={"sm": 6}, controls=[
        first_name_field, last_name_field, middle_name_field, group_field, age_field
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    content.controls.append(ft.Column(col={"sm": 6}, controls=[
        course_field, email_field, username_field, password_field, password2_field
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[register_button]))
    content.controls.append(ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[already_hav_account, login_button]
    ))

    container = ft.Container(shadow=ft.BoxShadow(
        color='grey', offset=ft.Offset(1, 2), blur_radius=10,
    ))
    container.bgcolor = ft.colors.WHITE
    container.border_radius = 8
    container.content = content
    container.width = 800
    # container.height = 700
    container.padding = ft.padding.all(20)
    container.border = ft.border.all(1, ft.colors.TRANSPARENT)

    return ft.View(
        scroll=ft.ScrollMode.AUTO,

        route='/register',
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[container]
    )
