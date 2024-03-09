import flet as ft
from flet import *

from constants import LOGO_PATH


class StudentAppBar(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.app_bar = ft.AppBar()
        self.app_bar.center_title = False
        self.app_bar.leading_width = 100
        self.app_bar.toolbar_height = 80
        self.app_bar.bgcolor = ft.colors.ORANGE_ACCENT

        self.back_button = ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW)
        self.back_button.on_click = lambda e: self.show_student_nav_view(e)

        self.log_out_button = ft.PopupMenuItem(text='Выход')
        self.log_out_button.on_click = lambda e: self.exit(e)
        self.app_bar_items = [
            self.log_out_button,
            ft.PopupMenuItem(),
            ft.PopupMenuItem(text='Настройки')
        ]

        self.app_bar_actions = ft.Container(
            content=ft.PopupMenuButton(items=self.app_bar_items),
            margin=ft.margin.only(left=50, right=25),
        )

        self.app_bar_title = ft.Row()

        self.appbar_title = ft.Row()
        self.appbar_title.alignment = ft.MainAxisAlignment.START
        self.appbar_title.spacing = 0
        self.appbar_title.controls = [
            self.back_button,
            ft.Container(width=10),
            ft.Image(LOGO_PATH, width=70, height=70),
            ft.Container(width=10),
            ft.Text('SDF', size=20, weight=ft.FontWeight.BOLD),
            ft.Text('Hub', size=20)
        ]
        self.title = self.appbar_title
        self.app_bar.actions = [self.app_bar_actions]

    def build(self):
        return ft.AppBar(
            title=self.appbar_title,
        )

    def show_student_nav_view(self, e) -> None:
        self.page.go('/student/main')

    def exit(self, e) -> None:
        self.page.session.set('is_auth', False)
        self.page.session.clear()
        self.page.go('/welcome')


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
        self.appbar_items = [
            self.log_out_button,
            PopupMenuItem(),
            PopupMenuItem(text='Настройки'),
        ]

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

        self.dlg = ft.AlertDialog(modal=True, actions=[
            ft.ElevatedButton('Да', on_click=lambda e: self.yes_click(e)),
            ft.ElevatedButton('Нет', on_click=lambda e: self.close_dlg(e)),
        ],
                                  actions_alignment=ft.MainAxisAlignment.CENTER)
        self.title = self.appbar_title
        self.actions = [self.appbar_actions]

    def close_dlg(self, e: ft.ControlEvent):
        self.dlg.open = False
        e.control.page.update()

    def yes_click(self, e: ft.ControlEvent):
        e.page.route = '/'
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
