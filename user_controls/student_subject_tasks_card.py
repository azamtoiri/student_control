# вспомогательный элемент для task_view, отображает каждое задание отдельно и для прикрепления файлов

import os.path
import shutil
from datetime import datetime

import flet as ft
from flet_core.file_picker import FilePickerFile

from database.database import StudentDatabase
from utils.banners import display_success_banner
from utils.routes_url import StudentRoutes
from utils.zip_file import compress_file_to_zip


class SubjectTile(ft.UserControl):
    def __init__(self, count, task_name, subject_task_id, user_id, enrollment_id, page):
        super().__init__()
        self.page = page
        self.count = count
        self.task_name = task_name
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
        self.completed = self.db.get_completed_task_status(self.user_id, self.subject_task_id)

    def build(self):
        if self.completed:
            return ft.ListTile(
                title=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f'{self.count}. {self.task_name}'),
                        ft.IconButton(
                            ref=self.icon_button,
                            icon=ft.icons.ADD_CIRCLE,
                            icon_color=ft.colors.SURFACE_TINT,
                            tooltip="удалить задание",
                            opacity=0.5,
                            on_click=lambda e: self.my_file_picker.pick_files(),
                        )
                    ]
                )
            )
        else:
            return ft.ListTile(
                title=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f'{self.count}. {self.task_name}'),
                        ft.IconButton(
                            ref=self.icon_button,
                            icon=ft.icons.ADD_CIRCLE,
                            icon_color=ft.colors.SURFACE_TINT,
                            tooltip='Отправить задание',
                            on_click=lambda e: self.my_file_picker.pick_files(),
                        )
                    ]
                )
            )

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
            if self.my_file_picker.result is not None and self.my_file_picker.result.files is not None:
                for f in self.my_file_picker.result.files:
                    uf.append(ft.FilePickerUploadFile(f.name, upload_url=self.page.get_upload_url(f.name, 600)))
                    print(uf)
            self.my_file_picker.upload(uf)

            for f in self.my_file_picker.result.files:
                ...
                # user_db.database.set_new_user_image(USER_ID, f.name)
                # user_avatar.change_user_image(f'/uploads/{f.name}')
                # user_avatar.update()
            self.page.update()
        else:
            task_file = self.db.get_completed_task_status(self.user_id, self.subject_task_id)
            if task_file:
                if os.path.exists(f'assets/uploads/{task_file.task_file}'):
                    os.remove(f'assets/uploads/{task_file.task_file}')
                self.db.delete_task_file(task_file)

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
    def __init__(
            self, user_id, subject_name, subject_id, page, file_picker: ft.FilePicker,
            theory_url
    ):
        super().__init__()
        self.page = page

        self.user_id = user_id
        self.db = StudentDatabase()
        self.subject_name = subject_name
        self.subject_id = subject_id
        self.file_picker = file_picker
        self.task_file_url = theory_url

        self.task_icon = ft.Icon(ft.icons.TASK_OUTLINED, color=ft.colors.SURFACE_TINT)
        self.subject_tasks = self.get_subject_tasks()
        self.file_picker.on_result = self.save_file_result

    def build(self):
        self.theory_button = ft.ElevatedButton(
            'Теория',
            on_click=lambda e: self.save_file_click(e),
            icon=ft.icons.DOWNLOAD
        )

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
                                    self.theory_button,
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

    def save_file_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            # Копирование файла
            shutil.copy2(f'assets/uploads/{self.task_file_url}', e.path)

    def save_file_click(self, e):
        if self.task_file_url is None:
            display_success_banner(self.page, 'Пока теории нет', ft.icons.ERROR)
            return
        else:
            self.file_picker.save_file(
                dialog_title='Скачать теорию', file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=['.pdf', '.docx', '.doc', '.txt'],
                file_name=self.task_file_url
            )
