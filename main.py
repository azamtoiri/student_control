import os

import flet as ft
import flet_fastapi

from database.database import UserDatabase
from user_controls.student_app_bar import STAppBar
from utils.lazy_db import LazyDatabase
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


user_db = LazyDatabase(UserDatabase)


async def main(page: ft.Page):
    page.title = 'Student Control'
    page.theme_mode = 'light'

    route = Routing(page=page, app_routes=all_routes, not_found_view=ViewNotFound, appbar=STAppBar(page), async_is=True)
    page.on_route_change = route.change_route
    # page.appbar = route.appbar
    page.session.set('username', 'admin')
    page.session.set('user_id', 6)
    page.session.set('is_auth', True)
    if page.session.get('user_id'):
        page.theme_mode = user_db.database.get_theme_mode(page.session.get('user_id'))
        page.theme = ft.Theme(color_scheme_seed=user_db.database.get_seed_color(page.session.get('user_id')))
        await page.update_async()
    # page.go('/home-edit')
    await page.go_async('/student/main')
    # page.go('/login')


assets_abs_path = os.path.abspath('assets')
uploads_abs_path = os.path.abspath('assets/uploads')

app = flet_fastapi.app(main, assets_dir=assets_abs_path, upload_dir=uploads_abs_path)
