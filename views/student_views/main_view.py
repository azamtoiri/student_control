import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.student_container import STContainer
from utils.routes_url import StudentRoutes, BaseRoutes


class Containers:
    def __init__(self):
        # TODO: Refactor code
        # home container
        self.home_container = STContainer(
            ft.Text('Домашняя страница', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6)
        # courses container
        self.courses_container = STContainer(
            content=ft.Text('Курсы', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6)
        self.grades_container = STContainer(
            content=ft.Text('Оценки', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6
        )
        self.tasks_container = STContainer(
            content=ft.Text('Задания', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6
        )
        self.to_do = STContainer(
            content=ft.Text('To-do', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6
        )
        self.exit_container = STContainer(
            content=ft.Text('Выйти', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15), col=6,
            alignment=ft.alignment.center
        )


dlg = ft.AlertDialog(modal=True, adaptive=True, actions_alignment=ft.MainAxisAlignment.CENTER)


def MainView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    #
    # Button
    #
    containers = Containers()

    # region: Functions
    async def home_click(e: ft.ControlEvent) -> None:
        await page.go_async(StudentRoutes.HOME_URL)

    async def courses_click(e: ft.ControlEvent) -> None:
        await page.go_async(StudentRoutes.SUBJECTS_URL)

    async def grades_click(e: ft.ControlEvent) -> None:
        await page.go_async(StudentRoutes.GRADES_URL)

    async def to_do_click(e: ft.ControlEvent) -> None:
        await page.go_async(StudentRoutes.TODO_URL)

    async def tasks_click(e: ft.ControlEvent) -> None:
        await page.go_async(StudentRoutes.TASKS_URL)

    async def close_dlg(e: ft.ControlEvent) -> None:
        dlg.open = False
        await e.page.update_async()

    async def yes_click(e: ft.ControlEvent) -> None:
        page.session.set('is_auth', False)
        page.session.clear()
        await page.go_async(BaseRoutes.INDEX_URL)
        await close_dlg(e)

    async def exit_click(e: ft.ControlEvent) -> None:
        dlg.title = ft.Text('Подтвердите действие')
        dlg.content = ft.Text('Вы точно хотите выйти?')
        dlg.actions = [
            ft.ElevatedButton('Да', on_click=yes_click, bgcolor=ft.colors.SURFACE_TINT,
                              color=ft.colors.WHITE,
                              ),
            ft.ElevatedButton('Нет', on_click=close_dlg, bgcolor=ft.colors.GREY,
                              color=ft.colors.WHITE)
        ]
        e.page.dialog = dlg
        dlg.open = True
        await e.page.update_async()

    # endregion

    # region: handlers
    containers.home_container.main_container.on_click = home_click
    containers.grades_container.main_container.on_click = grades_click
    containers.tasks_container.main_container.on_click = tasks_click
    containers.to_do.main_container.on_click = to_do_click
    containers.courses_container.main_container.on_click = courses_click
    containers.exit_container.main_container.on_click = exit_click

    # endregion

    logo_image = ft.Image(src=LOGO_PATH, width=200, height=200)
    student_title = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text('Fox', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.Text('Hub', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_ACCENT),
            ft.Text('Студент', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREY)
        ]
    )

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.MAIN_URL,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[logo_image, student_title]),
            ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(content=containers.home_container, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                    ft.Container(content=containers.grades_container, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                    ft.Container(content=containers.tasks_container, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                    ft.Container(content=containers.courses_container, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                    ft.Container(content=containers.to_do, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                    ft.Container(content=containers.exit_container, col={"sm": 6, "md": 4}, padding=20,
                                 alignment=ft.alignment.center),
                ]
            ),
        ]
    )
