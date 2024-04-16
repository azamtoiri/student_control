import flet as ft

from database.database import TeacherDatabase
from utils.exceptions import DontHaveGrades


class TeacherStudentsCard(ft.UserControl):
    def __init__(self, user_id, button_click):
        super().__init__()
        self.user_id = user_id
        self.button_click = button_click
        self.db = TeacherDatabase()
        self.count_of_grades_text = ft.Ref[ft.Text]()

        self.all_grades_count = 0

    async def get_all_grades_count(self):
        try:
            q = await self.db.get_teacher_students(self.user_id)
            self.all_grades_count = len(q)
        except DontHaveGrades as err:
            self.all_grades_count = 0

    def build(self):
        teachers_students = self.create_student_controls()

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GOLF_COURSE),
                            title=ft.Text(f'Кол-во студентов: {self.all_grades_count}',
                                          ref=self.count_of_grades_text)
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Студенты'),
                            controls=teachers_students
                        ),
                        ft.ListTile(
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Посмотреть всех студентов', text_align=ft.TextAlign.START),
                                    ft.IconButton(
                                        icon=ft.icons.NAVIGATE_NEXT, on_click=self.button_click,
                                        icon_color=ft.colors.SURFACE_TINT, bgcolor=ft.colors.SURFACE_VARIANT
                                    )
                                ]
                            ),
                        )
                    ]
                )
            )
        )

    def create_student_controls(self) -> list[ft.Control]:
        async def tt():
            await self.get_all_grades_count()

        all_subjects = []
        count = 1
        try:
            for i in self.db.get_teacher_students_no_async(user_id=self.user_id):
                all_subjects.append(
                    ft.ListTile(
                        title=ft.Text(f'{count}. {i[1]} {i[2]}'),
                    )
                )
                count += 1
            # return first 5 students
            return all_subjects[:5]
        except DontHaveGrades as ex:
            return []
