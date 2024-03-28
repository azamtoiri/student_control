#  Для отображения средней оценки по предметам

import flet as ft

from database.database import StudentDatabase
from utils.exceptions import DontHaveGrades


class AverageGradesCard(ft.UserControl):
    def __init__(self, user_id, button_clicked):
        super().__init__()
        self.user_id = user_id
        self.button_clicked = button_clicked
        self.db = StudentDatabase()

    def build(self):
        all_grades_count = self.db.get_all_grades(self.user_id)
        subjects_and_values = self.create_grades_controls()

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.STARS),
                            title=ft.Text(f'Всего оценок: {all_grades_count}')
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Средние оценки по предметам'),
                            controls=subjects_and_values
                        ),
                        ft.ListTile(
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Перейти к оценкам', text_align=ft.TextAlign.START),
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
        all = []
        try:
            for i in self.db.get_student_subjects(user_id=self.user_id):
                all.append(
                    ft.ListTile(
                        title=ft.Text(i[2]),
                        subtitle=ft.Text(
                            f'Средняя оценка {self.db.count_average_subject_grades(subject_name=i[2], user_id=self.user_id)}',
                            text_align=ft.TextAlign.END)
                    )
                )
            return all
        except DontHaveGrades as ex:
            return []
