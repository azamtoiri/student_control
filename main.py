import flet as ft
from utils.new_router import Routing
from views.routes import all_routes

from user_controls.student_app_bar import StudentAppBar, STAppBar


def main(page: ft.Page):
    page.title = 'Student Control'
    page.window_min_width = 700
    page.window_min_height = 900
    page.theme_mode = 'light'

    route = Routing(page=page, app_routes=all_routes)
    route.appbar = STAppBar()
    page.on_route_change = route.change_route
    page.appbar = route.appbar
    page.go('/')


ft.app(target=main)
