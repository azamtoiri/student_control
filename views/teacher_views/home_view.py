import os

import flet as ft
from flet_route import Basket, Params

from database.database import UserDatabase
from user_controls.teacher_controls import TeacherStudentsCard, TeacherSubjectsCard, TeacherExperience
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.create_container_home_view import create_container
from utils.lazy_db import LazyDatabase
from utils.routes_url import TeacherRoutes, BaseRoutes

user_db = LazyDatabase(UserDatabase)


# user_db = UserDatabase()


async def TeacherHomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    if len(page.views) > 2:
        page.views.pop()
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')
    DEFAULT_USER_IMAGE = '/default_user_image.png'

    user = user_db.database.get_user_by_id(USER_ID)

    # region: InputFields
    first_name_field = UserChangField(True, value=user.last_name, label='Фамилия')  # Фамилия
    last_name_field = UserChangField(True, value=user.first_name, label='Имя')  # Имя
    middle_name_field = UserChangField(True, value=user.middle_name, label='Отчество')  # Отчество
    group_field = UserChangField(True, value=user.group, label='Группа')  # Группа
    course_field = UserChangField(True, value=user.course, label='Курс')  # Звание
    age_field = UserChangField(True, value=user.age, label='Возраст')  # Возраст
    email_field = UserChangField(True, value=user.email, label='Email')  # Email
    username_text = UserChangField(True, value=user.username, label='Имя пользователя')

    # endregion

    user_image_dir = user_db.database.get_user_image_url(USER_ID)
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

    teachers_students_content = ft.Column(
        spacing=5, alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            TeacherStudentsCard(USER_ID, lambda e: page.go(page.views[-2].route)),
        ]
    )

    teachers_subjects_content = ft.Column(
        spacing=5, alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            TeacherSubjectsCard(USER_ID, lambda e: page.go(page.views[-2].route)),
        ]
    )

    teachers_experience_and_description_content = ft.Column(
        controls=[
            TeacherExperience(USER_ID, lambda e: page.go(BaseRoutes.HOME_EDIT_URL))
        ]
    )

    user_data_container = create_container(user_info_content)

    my_student_data_container = create_container(teachers_students_content, col={"sm": 12, "md": 6})

    my_subjects_data_container = create_container(teachers_subjects_content, col={"sm": 12, "md": 6})

    experience_container = create_container(teachers_experience_and_description_content)

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.HOME_URL,
        controls=[
            ft.Container(),
            user_data_container,
            experience_container,
            ft.ResponsiveRow(
                controls=[
                    my_student_data_container,
                    my_subjects_data_container,
                ]
            ),
        ]
    )
