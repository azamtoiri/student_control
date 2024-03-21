import flet as ft


def main(page: ft.Page) -> None:
    page.theme = ft.Theme(color_scheme_seed='green')
    page.theme_mode = 'light'

    todo_card = ft.Card(
        width=500,
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.TASK_ALT),
                        title=ft.Text('Имя предмета'),
                    ),
                    ft.ExpansionTile(
                        title=ft.Text('Задания'),
                        controls=[
                            ft.ListTile(
                                title=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text("Прочитать роман Преступление и наказание"),
                                        ft.Checkbox()
                                    ]
                                )
                            ),
                        ]
                    ),
                    ft.ListTile(
                        title=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text('Перейти к оценкам', text_align='start'),
                                ft.IconButton(icon=ft.icons.NAVIGATE_NEXT)
                            ]
                        ),
                    )
                ]
            )
        )
    )

    drop_down_icons = ft.Ref[ft.Dropdown]()

    def change_color_scheme_seed(e):
        drop_down_icons.current.visible = True

    icon_drop = ft.PopupMenuButton(
        icon=ft.icons.PALETTE_OUTLINED,
        menu_position=ft.PopupMenuPosition.UNDER,
        items=[
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
            ft.PopupMenuItem(icon=ft.icons.PALETTE_OUTLINED, text="Check power"),
        ]
    )

    page.add(
        ft.Row([icon_drop, ft.Text('Основные цвета')]),
        todo_card,
        ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("One-line list tile"),
                        ),
                        ft.ListTile(title=ft.Text("One-line dense list tile"), dense=True),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.SETTINGS),
                            title=ft.Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ft.ListTile(
                            leading=ft.Image(src="/icons/icon-192.png", fit="contain"),
                            title=ft.Text("One-line with leading control"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line with trailing control"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text("One-line with leading and trailing controls"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.SNOOZE),
                            title=ft.Text("Two-line with leading and trailing controls"),
                            subtitle=ft.Text("Here is a second title."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )
    )


ft.app(main, assets_dir='assets', upload_dir='assets/uploads')
