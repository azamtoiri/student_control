import flet as ft
from flet_route import Params, Basket

from database.database import TaskDatabase, UserDatabase
from database.models import Task as TaskDB


# TODO: bind to DB

class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete, task_id, completed: bool = False):
        super().__init__()
        self.db = TaskDatabase()
        self.completed = completed
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.task_id = task_id

    def build(self):
        self.display_task = ft.Checkbox(
            label=self.task_name, on_change=self.status_changed
        )
        self.display_task.value = self.completed
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(self.task_id, visible=False),
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Редактировать To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Удалить To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.db.updated_task(self.task_id, self.edit_name.value)
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.db.set_status(task_id=self.task_id, status=self.display_task.value)
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.UserControl):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db = TaskDatabase()
        self.tasks = ft.Column()
        self.load_tasks()

    def build(self):
        self.new_task = ft.TextField(
            hint_text="Что нужно сделать?", on_submit=self.add_clicked, expand=True
        )

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="все"), ft.Tab(text="активные"), ft.Tab(text="завершенные")],
        )

        self.items_left = ft.Text("0 задание не выполнено")
        self.items_left.visible = False

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Очистить все выполенные", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if self.new_task.value:
            task_instance = TaskDB(task_name=self.new_task.value, completed=False, user_id=self.user_id)
            added_task = self.db.add_task(task_instance)
            task = Task(self.new_task.value, self.task_status_change, self.task_delete, added_task.task_id)

            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.db.delete_task(task.controls[0].controls[0].controls[0].value)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def load_tasks(self):
        tasks = self.db.get_all_user_tasks(user_id=self.user_id)
        for task in tasks:
            _task = Task(task.task_name, self.task_status_change, self.task_delete, task.task_id,
                         completed=task.completed)
            self.tasks.controls.append(_task)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                    status == "все"
                    or (status == "активные" and task.completed == False)
                    or (status == "завершенные" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} задание не выполнено"
        self.items_left.visible = True
        super().update()


def TodoView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    username = page.session.get('username')
    user_id = UserDatabase().filter_users(username=username)[0].user_id
    app = TodoApp(user_id)
    return ft.View(
        # vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route='/todo',
        controls=[app]
    )
