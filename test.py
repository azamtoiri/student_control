import os
import shutil

import flet as ft


def main(page: ft.Page) -> None:
    page.scroll = ft.ScrollMode.AUTO

    def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        print("Selected files: ", e.files)
        upload_files(e)

    ft_image = ft.Image(src='uploads')

    def upload_files(e: ft.FilePickerUploadFile):
        if page.web:
            uf = []
            f: ft.FilePickerUploadFile
            for f in MyPickFiles.result.files:
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=page.get_upload_url(f.name, 600)))
            MyPickFiles.upload(uf)
            for f in MyPickFiles.result.files:
                ft_image.src = f'/uploads/{f.name}'
            page.update()
        else:
            for x in MyPickFiles.result.files:
                if os.path.exists(x.name):
                    os.remove(x.name)
                dest = os.path.join(os.getcwd(), "assets/uploads")
                shutil.copy(x.path, f'{dest}')
                ft_image.src = f'/uploads/{x.name}'

            page.update()

    MyPickFiles = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(MyPickFiles)
    page.update()

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft_image,
                ft.ElevatedButton(
                    'Choose files0', on_click=lambda _: MyPickFiles.pick_files()
                ),
                # ft.ElevatedButton("Upload", on_click=upload_files)
            ]
        )
    )


ft.app(main, assets_dir='assets', upload_dir='assets/uploads', view=ft.AppView.WEB_BROWSER)
