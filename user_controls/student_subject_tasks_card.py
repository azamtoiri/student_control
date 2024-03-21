import flet as ft

from database.database import StudentDatabase


class StudentSubjectTasksCard(ft.UserControl):
    def __init__(self, user_id, subject_name):
        super().__init__()
        self.user_id = user_id
        self.db = StudentDatabase()
        self.subject_name = subject_name

    def build(self):
        subject_tasks = self.get_subject_tasks()
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.TASK_ALT),
                            title=ft.Text(self.subject_name),
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Задания'),
                            controls=subject_tasks
                        ),
                    ]
                )
            )
        )

    def get_subject_tasks(self) -> list:
        res = []
        count = 1
        for value in self.db.get_student_subject_tasks_by_name(self.user_id, self.subject_name):
            res.append(ft.ListTile(
                title=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f'{count}. {value[0]}'),
                        ft.Checkbox(on_change=lambda e: self.change_task_status(e))
                    ]
                )
            ))
            count += 1
        return res

    def change_task_status(self, e: ft.ControlEvent) -> None:
        ...
