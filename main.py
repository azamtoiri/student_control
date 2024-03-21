import flet as ft

from user_controls.student_app_bar import STAppBar
from utils.new_router import Routing
from views.routes import all_routes


def ViewNotFound(page: ft.Page, params, basket):
    return ft.View(
        "/notfound/404",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                f"View {page.route} Page not found error 404",
                size=30,
            ),
            ft.TextButton(
                "Go Back OR ",
                on_click=lambda e: page.go(page.views[-2].route),
            )
        ]
    )


def main(page: ft.Page):
    page.title = 'Student Control'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN)

    route = Routing(page=page, app_routes=all_routes, not_found_view=ViewNotFound, appbar=STAppBar())
    # route.appbar = STAppBar()
    page.on_route_change = route.change_route
    # page.appbar = route.appbar
    page.session.set('username', 'mark123')
    page.session.set('user_id', 4)
    page.session.set('is_auth', True)
    # page.go('/home-edit')
    page.go('/subject/1')
    # page.go('/login')


ft.app(target=main, upload_dir="assets/uploads", assets_dir="assets")
