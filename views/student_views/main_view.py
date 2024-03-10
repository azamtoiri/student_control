import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.student_container import STContainer


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


def MainView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    #
    # Button
    #
    containers = Containers()

    # region: Functions
    def home_click(e: ft.ControlEvent) -> None:
        page.go('/student/home')

    def courses_click(e: ft.ControlEvent) -> None:
        page.go('/student/courses')

    def grades_click(e: ft.ControlEvent) -> None:
        page.go('/student/grades')

    def profile_click(e: ft.ControlEvent) -> None:
        page.go('/todo')

    def tasks_click(e: ft.ControlEvent) -> None:
        page.go('/student/tasks')

    def exit_click(e: ft.ControlEvent) -> None:
        page.session.clear()
        page.go('/')

    # endregion

    # region: handlers
    containers.home_container.main_container.on_click = lambda e: home_click(e)
    containers.grades_container.main_container.on_click = lambda e: grades_click(e)
    containers.tasks_container.main_container.on_click = lambda e: tasks_click(e)
    containers.to_do.main_container.on_click = lambda e: profile_click(e)
    containers.courses_container.main_container.on_click = lambda e: courses_click(e)
    containers.exit_container.main_container.on_click = lambda e: exit_click(e)

    # endregion

    logo_image = ft.Image(src=LOGO_PATH, width=200, height=200)
    # logo_image.top = 0
    # logo_image.left = 500
    # logo_image.expand = True

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route='/student/main',
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[logo_image]),
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
