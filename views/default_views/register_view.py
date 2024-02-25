import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.custom_input_field import CustomInputField
from user_controls.input_filter import TextOnlyInputFilterRu


def RegisterView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
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
    title.style = ft.TextThemeStyle.TITLE_MEDIUM
    title.text_align = ft.TextAlign.CENTER
    title.color = ft.colors.BLACK
    title.size = 20
    title.width = ft.FontWeight.BOLD
    title.expand = True

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
    register_button.width = 400
    register_button.height = 45
    register_button.icon = ft.icons.KEY

    login_button = ft.Container()
    login_button.alignment = ft.alignment.center
    login_button.content = ft.Text(
        value='Войти', size=15, color=ft.colors.with_opacity(0.5, ft.colors.BLUE)
    )
    # endregion

    # region: Some text
    already_hav_account = ft.Text("У  вас уже есть аккаунт")
    already_hav_account.size = 15
    already_hav_account.color = ft.colors.with_opacity(0.5, ft.colors.BLACK)
    # endregion

    fields_col = ft.Column([
        first_name_field,
        last_name_field,
        middle_name_field,
        group_field,
        course_field,
        age_field,
        email_field,
        username_field,
        password_field,
        password2_field
    ])
    fields_col.wrap = True
    fields_col.height = 450

    content = ft.Column()
    content.scroll = ft.ScrollMode.AUTO
    content.alignment = ft.MainAxisAlignment.CENTER
    content.controls.append(ft.Row([logo_icon]))
    content.controls.append(ft.Row([logo_text]))
    content.controls.append(ft.Row([title]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[fields_col]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[register_button]))
    content.controls.append(ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[already_hav_account, login_button]
    ))

    container = ft.Container()
    container.bgcolor = ft.colors.WHITE
    container.border_radius = 8
    container.content = content
    container.width = 800
    # container.height = 700
    container.padding = ft.padding.all(20)
    container.border = ft.border.all(1, ft.colors.TRANSPARENT)

    return ft.View(
        route='/register',
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[container]
    )
