import flet as ft


class ModalAlertDialog(ft.UserControl):
    def __init__(self, title: ft.Control, content: ft.Control, on_ok_click, on_cancel_click):
        super().__init__()
        self.title = title
        self.content = content
        self.on_ok_click = on_ok_click
        self.on_cancel_click = on_cancel_click

        self.actions = [
            ft.TextButton('Да', on_click=lambda e: self.on_ok_click(e)),
            ft.TextButton('Нет', on_click=lambda e: self.on_cancel_click(e))
        ]

    def build(self):
        self.dlg = ft.AlertDialog(
            title=self.title,
            content=self.content,
            actions=self.actions,
            modal=True,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            open=True
        )
        return self.dlg
