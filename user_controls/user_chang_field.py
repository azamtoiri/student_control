import flet as ft


class UserChangField(ft.UserControl):
    def __init__(self, disabled: bool, value, label: str = None, password: bool = False):
        super().__init__()
        self.disabled = disabled
        self.value = value
        self.label = label
        self.password = password

    def build(self):
        self.display_value = ft.TextField(
            value=self.value, disabled=True, label=self.label, col={"md": 6},
            expand=1,
            password=self.password,
            can_reveal_password=True,
        )

        self.edit_value = ft.TextField(label=self.label, expand=1)

        self.display_view = ft.Row(
            col={"sm": 6},
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_value,
                ft.IconButton(
                    icon=ft.icons.CREATE_OUTLINED,
                    tooltip="Редактировать",
                    on_click=self.edit_clicked,
                    visible=not self.disabled
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_value,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Изменить",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(col={"sm": 6}, controls=[self.display_view, self.edit_view])

    def save_clicked(self, e):
        self.display_value.value = self.edit_value.value
        # self.db.updated_task(self.task_id, self.edit_name.value)
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def edit_clicked(self, e):
        self.edit_value.value = self.display_value.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def change_value(self, new_value):
        self.display_value.value = new_value
        self.update()
