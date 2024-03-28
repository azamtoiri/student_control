# User avatar changing and showing with edit icon

import flet as ft


class UserImage(ft.UserControl):
    def __init__(self, image_dir, on_click=None, disabled: bool = True):
        super().__init__()
        self.image_dir = image_dir
        self.on_click = on_click
        self.ft_image = ft.Ref[ft.Image]()
        self.disabled = disabled

    def build(self):
        self.display_view = ft.Stack(
            controls=[
                ft.Image(
                    src=self.image_dir, width=180, height=180, border_radius=50,
                    ref=self.ft_image,
                    fit=ft.ImageFit.COVER
                ),
                ft.IconButton(
                    ft.icons.EDIT,
                    left=140, top=140,
                    # left=120, right=0, bottom=120, top=0,
                    on_click=self.on_click,
                    icon_color=ft.colors.SURFACE_VARIANT,
                    bgcolor=ft.colors.SURFACE_TINT,
                    opacity=0.75, icon_size=20,
                    tooltip='Изменить изображение',
                    visible=not self.disabled
                ),
            ]
        )
        return self.display_view

    def change_user_image(self, image_dir):
        self.ft_image.current.src = image_dir
        self.update()
