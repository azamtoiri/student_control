import flet as ft

from user_controls.modal_alert_dialog import ModalAlertDialog


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    dlg = ModalAlertDialog(
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        yes_click=lambda e: yes_click(e)
    )

    def yes_click(e: ft.ControlEvent):
        print("Yes clicked!")
        dlg.dlg.open = False
        dlg.update()

    def open_dlg_modal(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    page.add(
        ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
    )


ft.app(target=main)
