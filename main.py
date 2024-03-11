import flet as ft
import flet_fastapi

from user_controls.student_app_bar import STAppBar
from utils.new_router import Routing
from views.routes import all_routes


async def ViewNotFound(page: ft.Page, params, basket):
    async def go_back(e: ft.ControlEvent):
        await page.go_async(page.views[-2].route)

    return ft.View(
        "/notfound/404",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "View / Page not found error 404",
                size=30,
            ),
            ft.TextButton(
                "Go Back OR ",
                on_click=go_back
            )
        ]
    )


async def main(page: ft.Page):
    page.title = 'Student Control'
    # page.window_min_width = 700
    # page.window_min_height = 900
    page.theme_mode = 'light'

    route = Routing(page=page, app_routes=all_routes, not_found_view=ViewNotFound, async_is=True)
    route.appbar = STAppBar()
    page.on_route_change = route.change_route
    page.appbar = route.appbar
    page.session.set('username', 'admin')
    page.session.set('user_id', 1)
    page.session.set('is_auth', True)
    await page.go_async('/')


app = flet_fastapi.app(main)
