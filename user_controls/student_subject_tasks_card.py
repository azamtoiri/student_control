import os.path
from datetime import datetime

import flet as ft
from flet_core.file_picker import FilePickerFile

from database.database import StudentDatabase
from utils.banners import display_success_banner
from utils.routes_url import StudentRoutes
from utils.zip_file import compress_file_to_zip


class SubjectTile(ft.UserControl):
    def __init__(self, count, subject_name, subject_task_id, user_id, enrollment_id, page):
        super().__init__()
        self.page = page
        self.count = count
        self.subject_name = subject_name
        self.enrollment_id = enrollment_id
        self.user_id = user_id
        self.subject_task_id = subject_task_id
        self.icon_button = ft.Ref[ft.IconButton]()

        self.my_file_picker = ft.FilePicker(
            on_result=self.on_dialog_result,
        )
        self.page.overlay.append(self.my_file_picker)
        self.page.update()

        self.db = StudentDatabase()

    def build(self):
        return ft.ListTile(
            title=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f'{self.count}. {self.subject_name}'),
                    ft.IconButton(
                        ref=self.icon_button,
                        icon=ft.icons.ADD_CIRCLE,
                        icon_color=ft.colors.SURFACE_TINT,
                        tooltip='Отправить задание',
                        on_click=lambda e: self.my_file_picker.pick_files()
                    )
                ]
            )
        )

    def change_status(self, e: ft.ControlEvent, user_id, subject_task_id):
        self.update()

    def on_dialog_result(self, e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        try:
            self.upload_files(e)
            display_success_banner(self.page, 'Задание успешно отправлено', ft.icons.CHECK)
        except Exception as ex:
            print(ex)
        self.page.update()

    def upload_files(self, e: ft.FilePickerUploadEvent) -> None:
        uf = []
        if self.page.web:
            f: FilePickerFile
            for f in self.my_file_picker.result.files:
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=self.page.get_upload_url(f.name, 600)))
            self.my_file_picker.upload(uf)

            for f in self.my_file_picker.result.files:
                ...
                # user_db.database.set_new_user_image(USER_ID, f.name)
                # user_avatar.change_user_image(f'/uploads/{f.name}')
                # user_avatar.update()
            self.page.update()
        else:
            # task_file = self.db.get_completed_task_status(self.user_id, self.subject_task_id)
            # if task_file.completed:
            #     ...

            for x in self.my_file_picker.result.files:
                dest = os.path.join(os.getcwd(), "assets/uploads")
                # Создание нового имени файла с текущим временем
                new_filename = f"file_{self.page.session.get('username')}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{x.name}.zip"
                new_filepath = os.path.join(dest, new_filename)
                compress_file_to_zip(x.path, new_filepath)

                # here will be updating data in db
                self.db.add_subject_task_file(self.user_id, self.subject_task_id, self.enrollment_id, new_filename)
                self.page.update()
        self.icon_button.current.opacity = 0.5
        self.icon_button.current.tooltip = "Прикрепить новый файл"
        self.icon_button.current.update()


class StudentSubjectTasksCard(ft.UserControl):
    def __init__(self, user_id, subject_name, subject_id, page):
        super().__init__()
        self.page = page

        self.user_id = user_id
        self.db = StudentDatabase()
        self.subject_name = subject_name
        self.subject_id = subject_id

        self.task_icon = ft.Icon(ft.icons.TASK_OUTLINED, color=ft.colors.SURFACE_TINT)
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
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(self.subject_name),
                                    ft.ElevatedButton(
                                        'Теория', on_click=lambda e: self.theory_button_click(e)
                                    )
                                ]
                            ),
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Задания'),
                            controls=self.subject_tasks
                        ),
                    ]
                )
            )
        )

    def theory_button_click(self, e: ft.ControlEvent) -> None:
        e.page.route = f'{StudentRoutes.SIMPLE_SUBJECT_THEORY_URL}/{self.subject_id}'
        e.page.update()

    def get_subject_tasks(self) -> list:
        res = []
        count = 1

        for value in self.db.get_student_subject_tasks_by_name(self.user_id, self.subject_name):
            task_ = SubjectTile(
                count, value[0], value[1], self.user_id, page=self.page, enrollment_id=value[4]
            )
            res.append(task_)
            count += 1
        return res
