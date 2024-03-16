import os
import shutil

import flet as ft
from flet_route import Params, Basket

from database.database import UserDatabase
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.routes_url import StudentRoutes

user_db = UserDatabase()


def HomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # ref controls
    upload_button = ft.Ref[ft.ElevatedButton]()
    ft_image = ft.Ref[ft.Image]()

    # region: Functions
    def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        upload_files(e)
        page.update()

    def upload_files(e: ft.FilePickerUploadFile):
        uf = []
        if page.web:
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
                user_db.set_new_user_image(page.session.get('user_id'), _user_image_dir)
                user_avatar.ft_image.current.src = _user_image_dir
                user_avatar.update()
        page.update()

    # endregion

    # region: InputFields
    first_name_field = UserChangField(True, label="Фамилия *", value='Тест Фамилия')  # Фамилия
    last_name_field = UserChangField(True, label="Имя *", value='Тест Имя')  # Имя
    middle_name_field = UserChangField(True, label="Отчество *", value='Тест Отчество')  # Отчество
    group_field = UserChangField(True, label="Группа", value='Тест Группа')  # Группа
    course_field = UserChangField(True, label="Курс", value='Тест Курс')  # Звание
    age_field = UserChangField(True, label="Возраст", value='Возраст')  # Возраст
    email_field = UserChangField(True, label="Email", value='Тест Email')  # Email
    username_text = UserChangField(True, value=f'{page.session.get("username")}', label='Имя пользователя')

    # endregion

    pick_files = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_files)
    page.update()

    user_image_dir = user_db.get_user_image_url(page.session.get('user_id'))

    if (user_image_dir is None) or (os.path.exists(f'assets{user_image_dir}') is False):
        user_avatar = UserImage(
            f'/default_user_image.png',
            on_click=lambda _: pick_files.pick_files()
        )
    else:
        user_avatar = UserImage(
            user_image_dir,
            on_click=lambda _: pick_files.pick_files()
        )

    title = ft.Text('Домашняя страница', size=40, color=ft.colors.BLACK, text_align="center")

    # Background container for color and other
    main_container = ft.Container(
        bgcolor='white', border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    # main_container.content = content
    main_container.border_radius = 8
    main_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )
    content = ft.ResponsiveRow(spacing=5, alignment=ft.MainAxisAlignment.CENTER, controls=[
        ft.Column(col={"sm": 6, "md": 4},
                  controls=[user_avatar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[first_name_field, last_name_field, middle_name_field, group_field]),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[group_field, age_field, email_field, username_text]),
    ])
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
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[title]),
            main_container,
        ]
    )
