import flet as ft

from database.database import StudentDatabase


class SubjectDescription(ft.UserControl):
    def __init__(self, subject_id):
        super().__init__()
        self.subject_id = subject_id

    def build(self):
        self.database = StudentDatabase()
        self.subject_information = self.database.get_subject(self.subject_id)

        styled_title_container = ft.Container(
            expand=True, border_radius=8, ink=True, bgcolor=ft.colors.ORANGE_50,
            content=ft.Text(self.subject_information.subject_name, size=20, weight="bold"),
            alignment=ft.alignment.center, height=90
        )  # styled container for the title

        self.title = ft.Row(
            # alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                styled_title_container,
            ]
        )

        styled_description_container = ft.Container(
            expand=True, border_radius=8, bgcolor=ft.colors.GREY_100, height=200,
            content=ft.Text(self.subject_information.description, size=15), alignment=ft.alignment.top_left,
            padding=10
        )
        # teacher images gets from db with self.subject_information
        subject_image = ft.Image('../assets/Fox_Hub_logo.png', height=200, width=200, expand=0)
        teacher_image_and_fio = ft.Column(
            [
                ft.Image('../assets/Fox_Hub_logo.png', height=150, width=150),
                ft.Row([ft.Text('Имя преподавателя'), ft.Text('Фамилия')]),
                ft.Text('Опыт преподавателя'),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        styled_title_for_teacher = ft.Container(
            expand=True, border_radius=8, ink=True, bgcolor=ft.colors.YELLOW_50,
            content=ft.Text('Преподаватель', size=20, weight="bold"),
            alignment=ft.alignment.center, height=90
        )

        styled_teacher_information = ft.Container(
            expand=True, border_radius=8, bgcolor=ft.colors.GREY_100, height=200,
            content=ft.Column(
                [
                    ft.Text('Информация об учителе')
                ]
            ), alignment=ft.alignment.top_left,
            padding=10
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
