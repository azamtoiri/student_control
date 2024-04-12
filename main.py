import asyncio
import os
from pathlib import Path

import flet as ft
import flet.fastapi as flet_fastapi
from flet.fastapi import FletUpload
from flet.fastapi.flet_fastapi import Request

from constants import LOGO_PATH
from database.database import UserDatabase
from user_controls.bg_animation import Thing, ThingLightMode
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

# help classes
button_style: dict = {
    "expand": True,
    "height": 50,
    "bgcolor": "blue",
    "style": ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
    "color": "white"
}


class Button(ft.ElevatedButton):
    def __init__(self, text: str, on_click):
        super().__init__(**button_style, text=text, on_click=on_click)


body_style: dict = {
    "width": 400,
    "padding": 15,
    "bgcolor": ft.colors.with_opacity(0.045, "white"),
    "border_radius": 10,
    "shadow": ft.BoxShadow(
        spread_radius=20,
        blur_radius=45,
        color=ft.colors.with_opacity(0.45, "black"),
    )
}


class Body(ft.Container):
    def __init__(self):
        super().__init__(**body_style)
        self.logo = ft.Image(
            width=100,
            height=100,
            expand=True,
            src=LOGO_PATH,
        )
        self.logo_text = ft.Text(
            value="FoxHub",
            weight=ft.FontWeight.BOLD,
            color=ft.colors.with_opacity(1, "White"),
            size=30,
            expand=1,
            text_align="center"
        )

        self.welcome_text = ft.Text(
            value='Добро пожаловать',
            size=34,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
            expand=1
        )

        self.content = ft.Column(
            controls=[
                ft.Row([self.logo], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.logo_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Row([self.welcome_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Button('Вход', on_click=self.login_click)]),
                ft.Row([Button('Регистрация', on_click=self.register_click)]),
            ]
        )

    @staticmethod
    async def register_click(e: ft.ControlEvent) -> None:
        e.page.route = '/register'
        await cancel_running_tasks()  # Отменить все выполняющиеся задачи
        e.page.update()

    @staticmethod
    async def login_click(e: ft.ControlEvent) -> None:
        e.page.route = '/login'
        await cancel_running_tasks()  # Отменить все выполняющиеся задачи
        e.page.update()


async def cancel_running_tasks():
    global running_tasks
    for task in running_tasks:
        task.cancel()


async def main(page: ft.Page):
    page.title = 'Student Control'
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.theme_mode = ft.ThemeMode.DARK

    route = Routing(page=page, app_routes=all_routes, not_found_view=ViewNotFound, appbar=STAppBar(page), async_is=True)
    page.on_route_change = route.change_route

    if page.theme_mode == ft.ThemeMode.LIGHT:
        background = ft.Stack(
            expand=True,
            controls=[ThingLightMode() for _ in range(150)]
        )
    else:
        background = ft.Stack(
            expand=True,
            controls=[Thing() for _ in range(100)]
        )

    stack = ft.Stack(
        expand=True,
        controls=[
            background,
            ft.Column(
                alignment="center",
                horizontal_alignment="center",
                controls=[
                    ft.Row(alignment='center', controls=[Body()])
                ],
            ),
        ]
    )

    page.add(stack)
    page.update()

    if page.session.get('user_id'):
        page.theme_mode = user_db.database.get_theme_mode(page.session.get('user_id'))
        page.theme = ft.Theme(color_scheme_seed=user_db.database.get_seed_color(page.session.get('user_id')))
        page.update()

    global running_tasks  # Глобальный список для хранения выполняющихся задач
    running_tasks = [asyncio.create_task(item.animate_thing()) for item in background.controls]


assets_abs_path = os.path.abspath('assets')
uploads_abs_path = os.path.abspath('assets/uploads')
DOWNLOAD_PATH = str(Path.home())

app = flet_fastapi.app(main, assets_dir=assets_abs_path, upload_dir=uploads_abs_path)


@app.put("/upload")
async def flet_uploads(request: Request):
    await FletUpload(f"{DOWNLOAD_PATH}").handle(request)


if __name__ == '__main__':
    # uvicorn.run(app=app)
    ft.app(target=main, upload_dir='assets/uploads', assets_dir='assets')
