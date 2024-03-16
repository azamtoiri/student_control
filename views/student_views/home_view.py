import os
import shutil

import flet as ft
from flet_route import Params, Basket

from user_controls.user_image_picker import UserImage
from utils.routes_url import StudentRoutes


def HomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # ref controls
    upload_button = ft.Ref[ft.ElevatedButton]()
    ft_image = ft.Ref[ft.Image]()

    # region: Functions
    def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        upload_files(e)
        page.update()

    def upload_files(e: ft.FilePickerUploadFile):
        uf = []
        if page.web:
            for f in pick_files.result.files:
                # updating data in db
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=page.get_upload_url(f.name, 600)))
            pick_files.upload(uf)
        else:
            for x in pick_files.result.files:
                if os.path.exists(x.name):
                    os.remove(x.name)
                dest = os.path.join(os.getcwd(), "assets")
                shutil.copy(x.path, f'{dest}')

                # here will be updating data in db
                _user_image_dir = f'/{x.name}'
                user_avatar.ft_image.current.src = _user_image_dir
                user_avatar.update()
        page.update()

    # endregion

    pick_files = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_files)
    page.update()

    user_image_dir = "default_user_image.png"
    if user_image_dir != "":
        user_avatar = UserImage(
            f'/{user_image_dir}',
            on_click=lambda _: pick_files.pick_files(),
        )
    else:
        user_avatar = UserImage(
            '/default_user_image.png',
            on_click=lambda _: pick_files.pick_files(),
        )

    username_text = ft.Text(size=40, color='black', value=f'{page.session.get("username")}')

    content = ft.Column([
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.Text('Домашняя страница', size=40, color=ft.colors.BLACK)]
        ),
        ft.Row(controls=[user_avatar, username_text]),
    ])

    # Background container for color and other
    main_container = ft.Container(
        bgcolor='white', border_radius=8, padding=ft.padding.all(10)
    )
    main_container.content = content
    main_container.border_radius = 8
    main_container.shadow = ft.BoxShadow(
        color='grey',
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.HOME_URL,
        controls=[main_container]
    )
