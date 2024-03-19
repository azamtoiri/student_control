import os

import flet as ft
from flet_route import Params, Basket

from database.database import UserDatabase
from user_controls.todo_card import TodoCard
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.create_container_home_view import create_container
from utils.routes_url import StudentRoutes

user_db = UserDatabase()


def HomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    if len(page.views) > 1:
        page.views.pop()
    # Constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')
    DEFAULT_USER_IMAGE = '/default_user_image.png'

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

    user_image_dir = user_db.get_user_image_url(USER_ID)

    if (user_image_dir is None) or (os.path.exists(f'assets/uploads/{user_image_dir}') is False):
        user_avatar = UserImage(
            DEFAULT_USER_IMAGE,
        )
    else:
        user_avatar = UserImage(
            f'/uploads/{user_image_dir}',
        )

    title = ft.Text('Домашняя страница', size=40, color=ft.colors.BLACK, text_align=ft.TextAlign.CENTER)

    # region: Column Row ResponsiveRow with info data
    user_info_content = ft.ResponsiveRow(spacing=5, alignment=ft.MainAxisAlignment.CENTER, controls=[
        title,
        # ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[title]),
        ft.Column(col={"sm": 6, "md": 4},
                  controls=[user_avatar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[first_name_field, last_name_field, middle_name_field, course_field]),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[group_field, age_field, email_field, username_text]),
    ])

    def go_to_do(e):
        page.go(StudentRoutes.TODO_URL, skip_route_change_event=True)
        # page.views.reverse()

    # user_stat count of TODO
    todo_count = 1
    user_stat_info_content = TodoCard(
        todo_count, lambda e: go_to_do(e)
    )

    # endregion

    # region: Containers

    # user data container
    user_data_container = create_container(user_info_content)

    # first stats container
    user_stat_container = create_container(user_stat_info_content, col=6)

    # second stats info container
    user_stat2_container = create_container(user_info_content, col=6)

    # endregion

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.HOME_URL,
        controls=[
            ft.Container(),
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
