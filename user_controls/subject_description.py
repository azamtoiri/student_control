# отображения детальной информации
import asyncio

import flet as ft

from database.database import StudentDatabase
from user_controls.user_image_picker import UserImage
from utils.create_container_home_view import create_expand_container


class SubjectDescription(ft.UserControl):
    def __init__(self, subject_id):
        super().__init__()
        self.subject_id = subject_id

    def build(self):
        self.database = StudentDatabase()
        self.subject_information = asyncio.run(self.database.get_subject(self.subject_id))

        teacher_description = 'Пока нет информации о преподавателе'
        teacher_experience = 'неизвестно'

        if self.subject_information.users.teacher_info:
            if self.subject_information.users.teacher_info.teacher_experience is not None:
                teacher_experience = self.subject_information.users.teacher_info.teacher_experience

            if self.subject_information.users.teacher_info.teacher_description is not None:
                teacher_description = self.subject_information.users.teacher_info.teacher_description

        styled_title_container = ft.Container(
            expand=True, border_radius=8, ink=True, bgcolor=ft.colors.SURFACE_TINT, opacity=0.8,
            content=ft.Text(self.subject_information.subject_name, size=20, weight=ft.FontWeight.BOLD,
                            color=ft.colors.ON_INVERSE_SURFACE),
            alignment=ft.alignment.center, height=90
        )  # styled container for the title

        self.title = ft.Row(
            # alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                styled_title_container,
            ]
        )

        styled_description_container = create_expand_container(
            ft.Text(self.subject_information.description), height=200
        )
        # teacher images gets from db with self.subject_information
        if self.subject_information.users.user_image is not None:
            teacher_image = UserImage(
                f'/uploads/{self.subject_information.users.user_image}'
            )
        else:
            teacher_image = UserImage(
                '/default_user_image.png'
            )

        subject_image = ft.Image(
            f'/{self.subject_information.subject_image}', height=200, width=200
        )  # get_subject image
        teacher_image_and_fio = ft.Column(
            [
                teacher_image,
                # need url of teacher photo
                ft.Row(
                    controls=[
                        ft.Text(f'{self.subject_information.users.first_name}'),
                        ft.Text(f'{self.subject_information.users.middle_name}')
                    ]
                ),  # teacher information
                ft.Text(f'Стаж преподавателя: {teacher_experience}'),
                # teacher information
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        styled_title_for_teacher = ft.Container(
            expand=True, border_radius=8, ink=True, bgcolor=ft.colors.SURFACE_TINT, opacity=0.5,
            content=ft.Text(
                'О Преподавателе', size=20, weight=ft.FontWeight.BOLD,
                color=ft.colors.ON_INVERSE_SURFACE
            ),
            alignment=ft.alignment.center, height=90
        )

        if teacher_description == 'Пока нет информации о преподавателе':
            styled_teacher_information = create_expand_container(
                ft.Text(f'{teacher_description}'), height=200
            )
        else:
            styled_teacher_information = create_expand_container(
                ft.Text(f'{teacher_description}')
            )

        return ft.Column(
            controls=[
                self.title,  # the title of the subject
                ft.Row([subject_image, styled_description_container]),
                ft.Row([styled_title_for_teacher]),
                ft.Row([teacher_image_and_fio, styled_teacher_information]),
                # ft.Row([ft.Text('здесь будет темы курса')])
            ],
        )
