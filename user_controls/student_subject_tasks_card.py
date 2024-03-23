import flet as ft

from database.database import StudentDatabase


class SubjectTile(ft.UserControl):
    def __init__(self, count, subject_name, subject_task_id, user_id):
        super().__init__()
        self.count = count
        self.subject_name = subject_name
        self.user_id = user_id
        self.subject_task_id = subject_task_id

        self.db = StudentDatabase()

        self.check_box = ft.Checkbox(
            on_change=lambda e: self.change_status(e, user_id, subject_task_id),
            # set first view value from db
            value=bool(
                self.db.get_status_of_task_by_user_id(
                    user_id=self.user_id,
                    subject_task_id=self.subject_task_id
                )
            ),
            tooltip='изменить статус'
        )

    def build(self):
        return ft.ListTile(
            title=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f'{self.count}. {self.subject_name}'),
                    self.check_box
                ]
            )
        )

    def change_status(self, e: ft.ControlEvent, user_id, subject_task_id):
        self.db.change_task_status(user_id=user_id, subject_task_id=subject_task_id, value=self.check_box.value)
        self.update()


class StudentSubjectTasksCard(ft.UserControl):
    def __init__(self, user_id, subject_name):
        super().__init__()
        self.user_id = user_id
        self.db = StudentDatabase()
        self.subject_name = subject_name

        self.task_icon = ft.Icon(ft.icons.TASK_OUTLINED, color=ft.colors.SURFACE_TINT)
        self.true_check = []
        self.subject_tasks = self.get_subject_tasks()

    def build(self):
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=self.task_icon,
                            title=ft.Text(self.subject_name),
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Задания'),
                            controls=self.subject_tasks
                        ),
                    ]
                )
            )
        )

    def get_subject_tasks(self) -> list:
        res = []
        count = 1

        def change_task_status(e: ft.ControlEvent, subject_tasks_id) -> None:
            self.db.change_task_status(
                user_id=self.user_id,
                subject_task_id=subject_tasks_id,
                value=task_.check_box.value
            )

        for value in self.db.get_student_subject_tasks_by_name(self.user_id, self.subject_name):
            task_ = SubjectTile(
                count, value[0], value[1], self.user_id
            )
            res.append(task_)

            count += 1
            self.true_check.append(task_.check_box.value)

        self.update()
        return res

    def update(self):
        if all(self.true_check):
            self.task_icon.name = ft.icons.TASK
