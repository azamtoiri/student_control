import os
import shutil

import flet as ft
from flet_core.file_picker import FilePickerFile
from flet_route import Params, Basket

from database.database import UserDatabase
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.routes_url import StudentRoutes, TeacherRoutes

user_db = UserDatabase()


def HomeEditView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    # ref controls
    upload_button = ft.Ref[ft.ElevatedButton]()
    ft_image = ft.Ref[ft.Image]()

    # route
    main_page_url = TeacherRoutes.MAIN_URL if user_db.is_staff(USER_ID) else StudentRoutes.MAIN_URL

    # region: Functions
    def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        upload_files(e)
        page.update()

    def upload_files(e: ft.FilePickerUploadFile):
        uf = []
        if page.web:
            f: FilePickerFile
            for f in pick_files.result.files:
                # updating data in db
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=page.get_upload_url(f.name, 600)))
            pick_files.upload(uf)
        else:
            for x in pick_files.result.files:
                if os.path.exists(x.name):
                    os.remove(x.name)
                dest = os.path.join(os.getcwd(), "assets")
                shutil.copy(x.path, f'{dest}')

                # here will be updating data in db
                _user_image_dir = f'/{x.name}'
                user_db.set_new_user_image(USER_ID, _user_image_dir)
                user_avatar.ft_image.current.src = _user_image_dir
                user_avatar.update()
        page.update()

    # endregion
    class MixedCustomInputField(UserChangField):  # for rule DRY
        ...

    # region: InputFields
    first_name_field = MixedCustomInputField(False, label="Фамилия *", value='Тест Фамилия')  # Фамилия
    last_name_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Имя
    middle_name_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Отчество
    group_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Группа
    course_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Звание
    age_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Возраст
    email_field = MixedCustomInputField(False, label="Имя *", value='Тест Имя')  # Email
    username_text = UserChangField(disabled=True, value=f'{USERNAME}', label='Имя пользователя')

    # endregion

    pick_files = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_files)
    page.update()

    user_image_dir = user_db.get_user_image_url(USER_ID)

    if (user_image_dir is None) or (os.path.exists(f'assets{user_image_dir}') is False):
        user_avatar = UserImage(
            f'/default_user_image.png',
            on_click=lambda _: pick_files.pick_files(), disabled=False
        )
    else:
        user_avatar = UserImage(
            user_image_dir,
            on_click=lambda _: pick_files.pick_files(), disabled=False
        )

    content = ft.Column([
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text('Изменить профиль', size=40, color=ft.colors.BLACK),
                ft.OutlinedButton('На главную страницу', on_click=lambda _: page.go(main_page_url)),
            ]
        ),
        ft.Row(controls=[user_avatar, ft.Column(col={"sm": 6}, controls=[
            first_name_field, username_text
        ])]),
    ])

    # Background container for color and other
    main_container = ft.Container(
        bgcolor='white', border_radius=8, padding=ft.padding.all(10)
    )
    main_container.content = content
    main_container.border_radius = 8
    main_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.HOME_URL,
        controls=[main_container]
    )
