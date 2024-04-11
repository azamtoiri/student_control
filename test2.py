import shutil

import flet as ft


def main(page: ft.Page):
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            # Копирование файла
            shutil.copy2('assets/default_user_image.png', e.path)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)
    page.add(ft.ElevatedButton("Сохранить файл", on_click=lambda _: save_file_dialog.save_file(
        file_name="default_user_image.png",
    )))


ft.app(target=main)
