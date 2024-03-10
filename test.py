import flet as ft
from flet_core import Control

from fletrt import Route, NavigationRoute


class Index(NavigationRoute):
    def __init__(self):
        super().__init__()

        self.destinations = [
            '/home',
            '/settings'
        ]

    def navigation_bar(self) -> ft.NavigationBar:
        return ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(label='Home Page', icon=ft.icons.HOME),
                ft.NavigationDestination(label='Program Settings', icon=ft.icons.SETTINGS)
            ]
        )


class Home(Route):
    def body(self):
        content = ft.TextField(hint_text='Type anything...')
        confirm = ft.ElevatedButton('Go to next page with url parameters',
                                    on_click=lambda _: self.go('/home/' + content.value))

        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                content,
                confirm
            ]
        )

    def view(self) -> ft.View:
        view = super().view()

        view.vertical_alignment = ft.MainAxisAlignment.CENTER
        view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        return view


class Content(Route):
    def body(self) -> Control:
        return ft.Text('Content received via url: ' + self.route_params['content'])


class Settings(Route):

    def body(self):
        return ft.Column(
            controls=[
                ft.Text('Settings', size=100)
            ]
        )

    def view(self) -> ft.View:
        view = super().view()

        view.vertical_alignment = ft.MainAxisAlignment.CENTER
        view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        return view


def main(page: ft.Page):
    page.add(ft.ResponsiveRow([
        ft.Column(col={"sm": 6}, controls=[ft.Container(col={"sm": 6, "md": 4, "xl": 2},
                                                        content=ft.Text('Column 1'), bgcolor='white')]),
        ft.Column(col={"sm": 6}, controls=[ft.TextField()])
    ])

    )


ft.app(target=main)
