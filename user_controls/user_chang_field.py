from typing import Type, Callable

import flet as ft


class UserChangField(ft.UserControl):
    def __init__(
            self,
            disabled: bool,
            value,
            label: str = None,
            save_changes: Type[Callable] = None,
            read_only: bool = True,
    ):
        super().__init__()
        self.save_changes = save_changes
        self._disabled = disabled
        self.value = value
        self.label = label

        self.display_value = ft.TextField(
            value=self.value, label=self.label, col={"md": 6},
            expand=1, read_only=read_only, hint_text='Пусто',
            focused_border_color=ft.colors.ON_SURFACE_VARIANT, border_color=ft.colors.SURFACE_TINT
        )
        self.edit_value = ft.TextField(label=self.label, expand=1)

    def build(self):
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
                    visible=not self._disabled
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
        self.display_value.error_text = None
        # self.db.updated_task(self.task_id, self.edit_name.value)
        self.display_view.visible = True
        self.edit_view.visible = False
        self.save_changes(e)
        self.update()

    def edit_clicked(self, e):
        self.edit_value.value = self.display_value.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def change_value(self, new_value):
        self.display_value.value = new_value
        self.update()

    @property
    def get_value(self):
        return self.display_value.value

    def set_error_text(self, error_text):
        self.display_value.error_text = error_text
        self.update()
