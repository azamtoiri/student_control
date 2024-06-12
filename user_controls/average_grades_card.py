import asyncio

import flet as ft

from database.repositories import StudentRepository
from utils.exceptions import DontHaveGrades


class AverageGradesCard(ft.UserControl):
    def __init__(self, user_id, button_clicked):
        super().__init__()
        self.user_id = user_id
        self.button_clicked = button_clicked
        self.db = StudentRepository()
        self.all_grades_count = 'Загрузка...'
        self.subjects_and_values = ft.Ref[ft.ListTile]()
        self.average_subject_grades = ft.Ref[ft.ListTile]()
        asyncio.create_task(self.load_data())  # Начинаем загрузку данных в фоне

    async def load_data(self):
        print("LOADING")
        self.all_grades_count = await self.db.get_all_grades(self.user_id)
        self.subjects_and_values = await self.create_average_subject_tasks_grades()
        self.average_subject_grades = await self.create_average_subject_grades()

        print("LOADED", self.all_grades_count, self.subjects_and_values, self.average_subject_grades)
        self.update()
        await self.update_async()  # Обновляем интерфейс

    async def on_refresh_click(self, e):
        await self.load_data()

    def build(self):
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.STARS),
                            title=ft.Text(f'Всего оценок итоговых оценок: {self.all_grades_count}')
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Итоговые оценки по предметам'),
                            controls=self.average_subject_grades
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Средние оценки за задания по предметам'),
                            controls=self.subjects_and_values
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
                        ),
                        ft.ElevatedButton(
                            text="Обновить данные",
                            on_click=self.on_refresh_click
                        )
                    ]
                )
            )
        )

    async def create_average_subject_tasks_grades(self) -> list[ft.Control]:
        all = []
        try:
            student_subjects = await self.db.get_student_subjects(user_id=self.user_id)
            for i in student_subjects:
                average_grade = await self.db.count_average_tasks_subject_grade(subject_name=i[2], user_id=self.user_id)
                all.append(
                    ft.ListTile(
                        title=ft.Text(i[2]),
                        subtitle=ft.Row(
                            [
                                ft.Text(
                                    f'Средняя оценка:',
                                    text_align=ft.TextAlign.END
                                ),
                                ft.Text(
                                    f'{average_grade}',
                                    text_align=ft.TextAlign.END, weight=ft.FontWeight.BOLD, color=ft.colors.SURFACE_TINT
                                ),
                            ], alignment=ft.MainAxisAlignment.END
                        )
                    )
                )
            return all
        except DontHaveGrades as ex:
            return []

    async def create_average_subject_grades(self) -> list[ft.Control]:
        """Создание средней итоговой оценки по предметам"""
        all = []
        try:
            student_subjects = await self.db.get_student_subjects(user_id=self.user_id)
            for i in student_subjects:
                average_grades = await self.db.count_average_subject_grades(subject_name=i[2], user_id=self.user_id)
                all.append(
                    ft.ListTile(
                        title=ft.Text(i[2]),
                        subtitle=ft.Row(
                            [
                                ft.Text(
                                    f'Итоговая оценка: ',
                                    text_align=ft.TextAlign.END
                                ),
                                ft.Text(
                                    f'{average_grades}',
                                    text_align=ft.TextAlign.END, weight=ft.FontWeight.BOLD, color=ft.colors.SURFACE_TINT
                                ),
                            ], alignment=ft.MainAxisAlignment.END
                        )
                    )
                )
            return all
        except DontHaveGrades as ex:
            return []
