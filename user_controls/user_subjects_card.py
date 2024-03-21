import flet as ft

from database.database import StudentDatabase
from utils.exceptions import DontHaveGrades


class UserSubjectsCard(ft.UserControl):
    def __init__(self, user_id, button_clicked):
        super().__init__()
        self.user_id = user_id
        self.button_clicked = button_clicked
        self.db = StudentDatabase()
        self.count_of_grades_text = ft.Ref[ft.Text]()
        self.average_grades = ft.Ref[ft.Text]()
        try:
            self.all_grades_count = self.db.quantity_of_subjects(self.user_id)
        except DontHaveGrades as err:
            self.all_grades_count = 0

    def build(self):
        subjects_and_values = self.create_grades_controls()

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GOLF_COURSE),
                            title=ft.Text(f'Кол-во записанных курсов: {self.all_grades_count}',
                                          ref=self.count_of_grades_text)
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Курсы', ref=self.average_grades),
                            controls=subjects_and_values
                        ),
                        ft.ListTile(
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Перейти к курсам', text_align=ft.TextAlign.START),
                                    ft.IconButton(
                                        icon=ft.icons.NAVIGATE_NEXT, on_click=self.button_clicked,
                                        icon_color=ft.colors.SURFACE_TINT, bgcolor=ft.colors.SURFACE_VARIANT
                                    )
                                ]
                            ),
                        )
                    ]
                )
            )
        )

    def create_grades_controls(self) -> list[ft.Control]:
        all_subjects = []
        count = 1
        try:
            for i in self.db.get_student_subjects(user_id=self.user_id):
                all_subjects.append(
                    ft.ListTile(
                        title=ft.Text(f'{count}. {i[2]}'),
                    )
                )
                count += 1
            return all_subjects
        except DontHaveGrades as ex:
            return []
