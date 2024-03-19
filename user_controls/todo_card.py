import flet as ft


class TodoCard(ft.UserControl):
    def __init__(self, count, button_click):
        super().__init__()
        self.count = ft.Text(f'Кол-во не завершенных ToDo: {count}')
        self.button = ft.Ref[ft.IconButton]()
        self.button_click = button_click

    def build(self):
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.CHECKLIST),
                            title=self.count,
                            subtitle=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Перейти к ToDo'),
                                    ft.IconButton(
                                        ref=self.button,
                                        icon=ft.icons.NAVIGATE_NEXT,
                                        icon_color=ft.colors.ON_SURFACE_VARIANT,
                                        on_click=self.button_click
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )