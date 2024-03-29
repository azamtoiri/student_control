import flet as ft


class ModalAlertDialog(ft.UserControl):
    def __init__(self, title: ft.Control, content: ft.Control, yes_click):
        super().__init__()
        self.title = title
        self.content = content
        self.yes_click = yes_click

        self.dlg = ft.AlertDialog()

        self.actions = [
            ft.ElevatedButton('Да', on_click=lambda e: self.yes_click(e), bgcolor=ft.colors.SURFACE_TINT,
                              color=ft.colors.WHITE),
            ft.ElevatedButton('Нет', on_click=lambda e: self.on_cancel_click(e), bgcolor=ft.colors.GREY,
                              color=ft.colors.WHITE),
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

    def on_cancel_click(self, e: ft.ControlEvent):
        self.dlg.open = False
        self.dlg.update()
        e.page.update()
