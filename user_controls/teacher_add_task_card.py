import flet as ft

from database.database import StudentDatabase, StudentAsyncDatabase
from user_controls.modal_alert_dialog import ModalAlertDialog
from utils.banners import display_success_banner
from utils.display_error import display_form_error
from utils.exceptions import RequiredField


class SubjectTile(ft.UserControl):
    def __init__(self, count, task_name, subject_task_id, page):
        super().__init__()
        self.page = page
        self.count = count
        self.task_name = task_name
        self.subject_task_id = subject_task_id

        self.db = StudentDatabase()

        self.delete_dlg = ModalAlertDialog(
            title=ft.Text('Удаление задания'),
            content=ft.Text('Вы уверены, что хотите удалить задание?'),
            yes_click=lambda e: self.yes_delete_task(e)
        )

    def build(self):
        return ft.ListTile(
            title=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f'{self.count}. {self.task_name}'),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.SURFACE_TINT,
                        tooltip="Прикрепить новый файл",
                        on_click=lambda e: self.open_dialog(e)
                    )
                ]
            )
        )

    def open_dialog(self, e: ft.ControlEvent):
        self.page.dialog = self.delete_dlg
        self.delete_dlg.dlg.open = True
        self.page.update()
        self.delete_dlg.update()

    def remove_task(self, e: ft.ControlEvent) -> None:
        self.db.delete_teacher_subject_task(self.subject_task_id)
        e.page.update()

    def yes_delete_task(self, e: ft.ControlEvent):
        self.remove_task(e)
        self.delete_dlg.dlg.open = False
        self.delete_dlg.update()
        self.page.update()


class TeacherAddTaskCard(ft.UserControl):
    def __init__(self, user_id, subject_name, subject_id, page):
        super().__init__()
        self.page = page

        self.user_id = user_id
        self.db = StudentDatabase()
        self.subject_name = subject_name
        self.subject_id = subject_id

        self.task_name_field = ft.TextField(
            label='Название задания',
        )
        self.add_task_button = ft.ElevatedButton(
            'Добавить задание',
            on_click=lambda e: self.add_task_button_click(e)
        )

        self.dlg_add_text = ft.Text('Введите название задания')
        self.add_task_dlg = ModalAlertDialog(
            title=ft.Text(f'{subject_name}', expand=1, text_align=ft.TextAlign.CENTER),
            content=ft.Column(
                height=100,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.dlg_add_text,
                    self.task_name_field,
                ]
            ),
            yes_click=lambda e: self.yes_add_task(e)
        )

        self.task_icon = ft.Icon(ft.icons.TASK_OUTLINED, color=ft.colors.SURFACE_TINT)
        self.subject_tasks = self.get_subject_tasks()

        # Subject tasks_tile
        self.expansion_tile = ft.ExpansionTile(
            controls=self.subject_tasks,
            title=ft.Text('Задания'),
            on_change=lambda e: self.update_expansion_tile(e)
        )

    def yes_add_task(self, e: ft.ControlEvent) -> None:
        task_name = str(self.task_name_field.value).strip() if len(self.task_name_field.value) else None
        fields = {
            'task_name': self.task_name_field,
        }
        try:
            self.db.add_teacher_subject_task(self.subject_id, task_name)
            self.add_task_dlg.dlg.open = False
            self.add_task_dlg.update()
            display_success_banner(self.page, 'Задание успешно добавлено', ft.icons.CHECK)
            e.page.update()
        except RequiredField as error:
            display_form_error(self.page, str(error), fields)
            e.page.update()

        self.page.update()

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
                                        'Добавить задание', on_click=lambda e: self.add_task_button_click(e)
                                    )
                                ]
                            ),
                        ),
                        self.expansion_tile,
                    ]
                )
            )
        )

    def add_task_button_click(self, e: ft.ControlEvent) -> None:
        self.page.dialog = self.add_task_dlg
        if self.task_name_field.value:
            self.task_name_field.value = None
        self.add_task_dlg.dlg.open = True
        self.page.update()
        self.add_task_dlg.dlg.update()

    def get_subject_tasks(self) -> list:
        res = []
        count = 1

        for value in self.db.get_teacher_subject_tasks(self.user_id, subject_id=self.subject_id):
            task_ = SubjectTile(
                count=count, task_name=value[4],
                subject_task_id=value[5], page=self.page
            )
            count += 1
            res.append(task_)
        return res

    def update_expansion_tile(self, e: ft.ControlEvent) -> None:
        teacher_tasks_len = len(self.db.get_teacher_subject_tasks(self.user_id, self.subject_id))
        current_subject_len = len(self.subject_tasks)
        if e.data == 'false':
            return
        if teacher_tasks_len <= current_subject_len <= teacher_tasks_len:
            return
        count = 1
        self.expansion_tile.controls.clear()

        for value in self.db.get_teacher_subject_tasks(self.user_id, subject_id=self.subject_id):
            task_ = SubjectTile(
                count=count, task_name=value[4],
                subject_task_id=value[5], page=self.page
            )
            self.expansion_tile.controls.append(task_)
            count += 1
        self.expansion_tile.update()
        e.page.update()


async def create_teacher_add_task_card(user_id, subject_name, subject_id, page):
    async_db = StudentAsyncDatabase()

    async def yes_add_task(e):
        task_name = str(task_name_field.value).strip() if len(task_name_field.value) else None
        fields = {
            'task_name': task_name_field,
        }
        try:
            await async_db.add_teacher_subject_task(subject_id, task_name)
            add_task_dlg.dlg.open = False
            add_task_dlg.update()
            display_success_banner(page, 'Задание успешно добавлено', ft.icons.CHECK)
            e.page.update()
        except RequiredField as error:
            display_form_error(page, str(error), fields)
            e.page.update()

        page.update()

    async def add_task_button_click(e):
        page.dialog = add_task_dlg
        if task_name_field.value:
            task_name_field.value = None
        add_task_dlg.dlg.open = True
        page.update()
        add_task_dlg.dlg.update()

    async def get_subject_tasks():
        res = []
        count = 1

        values = await async_db.get_teacher_subject_tasks(user_id, subject_id)
        for value in values:
            task_ = SubjectTile(
                count=count, task_name=value[4],
                subject_task_id=value[5], page=page
            )
            count += 1
            res.append(task_)
        return res

    async def update_expansion_tile(e):
        teacher_tasks_len = len(await async_db.get_teacher_subject_tasks(user_id, subject_id))
        current_subject_len = len(subject_tasks)
        if e.data == 'false':
            return
        if teacher_tasks_len <= current_subject_len <= teacher_tasks_len:
            return
        count = 1
        expansion_tile.controls.clear()
        values = await async_db.get_teacher_subject_tasks(user_id, subject_id=subject_id)
        for value in values:
            task_ = SubjectTile(
                count=count, task_name=value[4],
                subject_task_id=value[5], page=page
            )
            expansion_tile.controls.append(task_)
            count += 1
        expansion_tile.update()
        e.page.update()

    task_name_field = ft.TextField(label='Название задания')
    add_task_button = ft.ElevatedButton('Добавить задание', on_click=add_task_button_click)

    dlg_add_text = ft.Text('Введите название задания')
    add_task_dlg = ModalAlertDialog(
        title=ft.Text(f'{subject_name}', expand=1, text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            height=100,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                dlg_add_text,
                task_name_field,
            ]
        ),
        yes_click=yes_add_task
    )

    task_icon = ft.Icon(ft.icons.TASK_OUTLINED, color=ft.colors.SURFACE_TINT)
    subject_tasks = await get_subject_tasks(user_id, subject_id, page)

    expansion_tile = ft.ExpansionTile(
        controls=subject_tasks,
        title=ft.Text('Задания'),
        on_change=update_expansion_tile
    )

    return ft.Card(
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=[
                    ft.ListTile(
                        leading=task_icon,
                        title=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(subject_name),
                                ft.ElevatedButton('Добавить задание', on_click=add_task_button_click)
                            ]
                        ),
                    ),
                    expansion_tile,
                ]
            )
        )
    )
