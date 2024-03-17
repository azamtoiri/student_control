import os

import flet as ft
from flet_route import Params, Basket

from database.database import UserDatabase
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.routes_url import StudentRoutes

user_db = UserDatabase()


def HomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # Constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    # ref controls
    upload_button = ft.Ref[ft.ElevatedButton]()
    ft_image = ft.Ref[ft.Image]()

    # region: Functions

    # endregion

    user = user_db.get_user_by_id(USER_ID)

    # region: InputFields
    first_name_field = UserChangField(True, value=user.first_name, label='Фамилия')  # Фамилия
    last_name_field = UserChangField(True, value=user.last_name, label='Имя')  # Имя
    middle_name_field = UserChangField(True, value=user.middle_name, label='Отчество')  # Отчество
    group_field = UserChangField(True, value=user.group, label='Группа')  # Группа
    course_field = UserChangField(True, value=user.course, label='Курс')  # Звание
    age_field = UserChangField(True, value=user.age, label='Возраст')  # Возраст
    email_field = UserChangField(True, value=user.email, label='Email')  # Email
    username_text = UserChangField(True, value=user.username, label='Имя пользователя')

    # endregion

    user_image_dir = user_db.get_user_image_url(page.session.get('user_id'))

    if (user_image_dir is None) or (os.path.exists(f'assets/uploads/{user_image_dir}') is False):
        user_avatar = UserImage(
            f'/default_user_image.png',
        )
    else:
        user_avatar = UserImage(
            f'/uploads/{user_image_dir}',
        )

    title = ft.Text('Домашняя страница', size=40, color=ft.colors.BLACK, text_align="center")

    # Background container for color and other
    user_data_container = ft.Container(
        bgcolor='white', border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    user_stat_container = ft.Container(
        col={"sm": 6},
        bgcolor='white', border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    user_stat2_container = ft.Container(
        col={"sm": 6},
        bgcolor='white', border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    # main_container.content = content
    user_data_container.border_radius = 8
    user_data_container.shadow = ft.BoxShadow(
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
    user_data_container.content = content
    user_data_container.border_radius = 8
    user_data_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )

    user_stat_container.content = content
    user_stat_container.border_radius = 8
    user_stat_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )
    user_stat2_container.content = content
    user_stat2_container.border_radius = 8
    user_stat2_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )
    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.HOME_URL,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[title]),
            user_data_container,
            ft.ResponsiveRow(
                spacing=5,
                controls=[
                    user_stat_container,
                    user_stat2_container
                ]
            )
        ]
    )
