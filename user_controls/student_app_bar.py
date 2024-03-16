import flet as ft
from flet import *

from constants import LOGO_PATH
from utils.routes_url import BaseRoutes, StudentRoutes, TeacherRoutes


class STAppBar(AppBar):
    """
    Custom app bar, for all Students views
    """

    def __init__(self) -> None:
        super().__init__()
        self.center_title = False
        self.leading_width = 100
        self.toolbar_height = 80
        self.bgcolor = colors.ORANGE_ACCENT
        self.adaptive = True

        self.log_out_button = PopupMenuItem(text='Выход')
        self.log_out_button.on_click = lambda e: self.log_out(e)
        self.edit_view_button = PopupMenuItem(text='Изменить профиль')
        self.edit_view_button.on_click = lambda e: self.edit_view_click(e)
        self.appbar_items = [
            self.edit_view_button,
            PopupMenuItem(),
            self.log_out_button,
        ]
        self.adaptive = True

        self.appbar_actions = Container(
            content=PopupMenuButton(
                items=self.appbar_items,
            ),
            margin=margin.only(left=50, right=25),
        )

        self.appbar_title = Row()
        self.appbar_title.alignment = MainAxisAlignment.START
        self.appbar_title.spacing = 0
        self.appbar_title.controls = [
            Container(width=10),
            Image(LOGO_PATH, width=70, height=70),
            Container(width=10),
            Text('FOX', size=20, weight=FontWeight.BOLD),
            Text('Hub', size=20)
        ]

        self.dlg = ft.AlertDialog(modal=True, adaptive=True, actions=[
            ft.ElevatedButton('Да', on_click=lambda e: self.yes_click(e), bgcolor=ft.colors.GREEN,
                              color=ft.colors.WHITE),
            ft.ElevatedButton('Нет', on_click=lambda e: self.close_dlg(e), bgcolor=ft.colors.GREY,
                              color=ft.colors.WHITE),
        ],
                                  actions_alignment=ft.MainAxisAlignment.CENTER)
        self.title = self.appbar_title
        self.actions = [self.appbar_actions]

    def close_dlg(self, e: ft.ControlEvent):
        self.dlg.open = False
        e.control.page.update()

    def yes_click(self, e: ft.ControlEvent):
        e.page.route = BaseRoutes.INDEX_URL
        e.page.session.clear()
        e.page.update()
        self.close_dlg(e)
        self.page.session.clear()

    def log_out(self, e: ft.ControlEvent) -> None:
        self.dlg.title = ft.Text('Подтвердите действие')
        self.dlg.content = ft.Text('Вы точно хотите выйти?')
        e.page.dialog = self.dlg
        self.dlg.open = True
        e.page.update()

    def edit_view_click(self, e: ft.ControlEvent) -> None:
        self.edit_view_button.disabled = False
        e.page.route = BaseRoutes.HOME_EDIT_URL
        e.page.update()
