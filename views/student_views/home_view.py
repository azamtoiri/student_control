import flet as ft
from flet_route import Params, Basket


def HomeView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # region: Functions

    # endregion

    _user_avatar = ft.CircleAvatar(
        radius=110,
        foreground_image_url="assets/Fox_Hub_logo.png",
    )

    user_avatar = ft.Container(padding=ft.padding.all(10), bgcolor='grey', border_radius=150)
    user_avatar.content = _user_avatar

    username_text = ft.Text(size=40, color='black', value=f'{page.session.get("username")}')

    content = ft.Column([
        ft.Row(alignment=ft.MainAxisAlignment.CENTER,
               controls=[ft.Text('Домашняя страница', size=40, color=ft.colors.BLACK)]),
        ft.Row([
            ft.Container(content=user_avatar, padding=ft.padding.only(top=50, left=40, right=20)),
            username_text,
        ],
            alignment=ft.MainAxisAlignment.START, expand=False
        ),

        ft.Row([
            ft.Container(width=100, height=100, bgcolor='grey')
        ],
            expand=True
        )
    ])

    # Background container for color and other
    main_container = ft.Container(bgcolor='white', border_radius=8, padding=ft.padding.all(10))
    main_container.content = content
    main_container.expand = True
    main_container.border_radius = 8
    main_container.shadow = ft.BoxShadow(
        color='grey', offset=ft.Offset(1, 2), blur_radius=10,
    )

    return ft.View(
        route='/student/home',
        controls=[main_container]
    )
