import flet as ft

from database.database import UserDatabase
from user_controls.student_app_bar import STAppBar
from utils.lazy_db import LazyDatabase
from utils.new_router import Routing
from views.routes import all_routes


def ViewNotFound(page: ft.Page, params, basket):
    return ft.View(
        "/notfound/404",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                f"{page.route} Page not found error 404",
                size=30,
            ),
            ft.TextButton(
                "Go Back OR ",
                on_click=lambda e: page.go(page.views[-2].route),
            )
        ]
    )


user_db = LazyDatabase(UserDatabase)


def main(page: ft.Page):
    page.title = 'Student Control'
    page.theme_mode = ft.ThemeMode.LIGHT

    route = Routing(page=page, app_routes=all_routes, not_found_view=ViewNotFound, appbar=STAppBar(page))
    # route.appbar = STAppBar()
    page.on_route_change = route.change_route
    # page.appbar = route.appbar
    page.session.set('username', 'jane123')
    page.session.set('user_id', 2)
    page.session.set('is_auth', True)
    page.session.set('is_staff', True)
    if page.session.get('user_id'):
        page.theme_mode = user_db.database.get_theme_mode(page.session.get('user_id'))
        page.theme = ft.Theme(color_scheme_seed=user_db.database.get_seed_color(page.session.get('user_id')))
        page.update()
    page.go('/teacher/my-subjects')
    # page.go('/teacher/home')
    # page.go('/subject/1')


ft.app(target=main, upload_dir="assets/uploads", assets_dir="assets")
