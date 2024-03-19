import flet as ft
from flet import *

from constants import LOGO_PATH
from utils.routes_url import BaseRoutes


class STAppBar(AppBar):
    """
    Custom app bar, for all Students views
    """

    def __init__(self) -> None:
        super().__init__()
        self.center_title = False
        self.leading_width = 100
        self.toolbar_height = 80
        self.bgcolor = colors.SURFACE_TINT
        self.adaptive = True

        self.log_out_button = PopupMenuItem(text='Выход', icon=ft.icons.EXIT_TO_APP)
        self.log_out_button.on_click = lambda e: self.log_out(e)
        self.edit_view_button = PopupMenuItem(text='Изменить профиль', icon=ft.icons.SETTINGS)
        self.edit_view_button.on_click = lambda e: self.edit_view_click(e)
        self.change_theme_mode_button = ft.Ref[ft.PopupMenuItem]()

        self.appbar_items = [
            self.edit_view_button,
            ft.PopupMenuItem(
                ref=self.change_theme_mode_button,
                on_click=lambda e: self.change_theme_mode(e),
                icon=ft.icons.DARK_MODE,
                text='Темная тема'
            ),
            self.log_out_button,
        ]

        self.color_scheme_pop_menu_icon = ft.Ref[ft.Icon]()
        self.deep_purple_color_button = ft.Ref[ft.PopupMenuItem]()
        self.indigo_color_button = ft.Ref[ft.PopupMenuItem]()
        self.blue_color_button = ft.Ref[ft.PopupMenuItem]()
        self.teal_color_button = ft.Ref[ft.PopupMenuItem]()
        self.green_color_button = ft.Ref[ft.PopupMenuItem]()
        self.yellow_color_button = ft.Ref[ft.PopupMenuItem]()
        self.orange_color_button = ft.Ref[ft.PopupMenuItem]()
        self.deep_orange_color_button = ft.Ref[ft.PopupMenuItem]()
        self.pink_color_button = ft.Ref[ft.PopupMenuItem]()

        self.appbar_actions = ft.Row(
            [
                PopupMenuButton(
                    content=ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.INVERSE_SURFACE,
                                    ref=self.color_scheme_pop_menu_icon),
                    items=[
                        PopupMenuItem(ref=self.deep_purple_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.DEEP_PURPLE),
                            ft.Text('Темно-фиолетовый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.DEEP_PURPLE)),

                        PopupMenuItem(ref=self.indigo_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.INDIGO),
                            ft.Text('Индиго')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.INDIGO)),

                        PopupMenuItem(ref=self.blue_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.BLUE),
                            ft.Text('Синий (базовый)')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.BLUE)),

                        PopupMenuItem(ref=self.teal_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.TEAL),
                            ft.Text('Бирюзовый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.TEAL)),

                        PopupMenuItem(ref=self.green_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.GREEN),
                            ft.Text('Зеленый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.GREEN)),

                        PopupMenuItem(ref=self.green_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.YELLOW),
                            ft.Text('Желтый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.YELLOW)),

                        PopupMenuItem(ref=self.orange_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.ORANGE),
                            ft.Text('Оранжевый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.ORANGE)),

                        PopupMenuItem(ref=self.deep_orange_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.DEEP_ORANGE),
                            ft.Text('Темно-оранжевый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.DEEP_ORANGE)),

                        PopupMenuItem(ref=self.pink_color_button, content=ft.Row([
                            ft.Icon(ft.icons.PALETTE_OUTLINED, color=ft.colors.PINK),
                            ft.Text('Розовый')
                        ]), on_click=lambda e: self.change_seed_color(e, ft.colors.PINK)),
                    ]
                ),
                ft.Text('Цвет интерфейса', color=ft.colors.INVERSE_SURFACE),
                Container(
                    content=PopupMenuButton(
                        content=ft.Icon(ft.icons.MENU, color=ft.colors.INVERSE_SURFACE),
                        items=self.appbar_items,
                    ),
                    margin=margin.only(right=25)
                ),
            ]
        )

        self.appbar_title = Row()
        self.appbar_title.alignment = MainAxisAlignment.START
        self.appbar_title.spacing = 0
        self.appbar_title.controls = [
            Container(width=10),
            Image(LOGO_PATH, width=70, height=70),
            Container(width=10),
            Text('FOX', size=20, weight=FontWeight.BOLD, color=ft.colors.INVERSE_SURFACE),
            Text('Hub', size=20, color=ft.colors.INVERSE_SURFACE)
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

    def log_out(self, e: ft.ControlEvent) -> None:
        self.dlg.title = ft.Text('Подтвердите действие')
        self.dlg.content = ft.Text('Вы точно хотите выйти?')
        e.page.dialog = self.dlg
        self.dlg.open = True
        e.page.update()

    def edit_view_click(self, e: ft.ControlEvent) -> None:
        self.edit_view_button._disabled = False
        e.page.route = BaseRoutes.HOME_EDIT_URL
        e.page.update()

    def change_seed_color(self, e: ft.ControlEvent, color: ft.colors) -> None:
        e.page.theme = ft.Theme(color_scheme_seed=color)
        e.page.update()
        self.update()

    def change_theme_mode(self, e: ft.ControlEvent):
        if e.page.theme_mode == ft.ThemeMode.DARK:
            e.page.theme_mode = ft.ThemeMode.LIGHT
            self.change_theme_mode_button.current.icon = ft.icons.DARK_MODE
            self.change_theme_mode_button.current.text = 'Темная тема'
            e.page.update()
            self.update()
        else:
            e.page.theme_mode = ft.ThemeMode.DARK
            self.change_theme_mode_button.current.icon = ft.icons.LIGHT_MODE
            self.change_theme_mode_button.current.text = 'Светлая тема'
            e.page.update()
            self.update()
