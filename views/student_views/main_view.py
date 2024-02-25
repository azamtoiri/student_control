import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.student_container import STContainer


class Containers:
    def __init__(self):
        # TODO: Refactor code
        # home container
        self.home_container = STContainer(ft.Text('Домашняя страница', color=ft.colors.BLACK),
                                          alignment=ft.alignment.center)

        # courses container
        self.courses_container = STContainer(content=ft.Text('Курсы', size=14, color=ft.colors.BLACK),
                                             alignment=ft.alignment.center)
        self.grades_container = STContainer(content=ft.Text('Оценки', size=14, color=ft.colors.BLACK),
                                            alignment=ft.alignment.center)
        self.tasks_container = STContainer(content=ft.Text('Задания', size=14, color=ft.colors.BLACK),
                                           alignment=ft.alignment.center)
        self.profile_container = STContainer(ft.Text('Профиль', color=ft.colors.BLACK), alignment=ft.alignment.center)


def MainView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    #
    # Button
    #
    containers = Containers()

    # region: handlers
    containers.home_container.main_container.on_click = lambda _: page.go('/student/home')
    containers.grades_container.main_container.on_click = lambda _: page.go('/student/grades')
    containers.tasks_container.main_container.on_click = lambda _: page.go('/student/tasks')
    containers.profile_container.main_container.on_click = lambda _: page.go('/student/profile')
    containers.courses_container.main_container.on_click = lambda _: page.go('/student/courses')
    # endregion

    def on_hover(e: ft.HoverEvent):
        """Container on hove"""
        if e.control.scale != 1.120:
            e.control.scale = 1.120
        else:
            e.control.scale = 1
        e.control.update()
        return ft.View(
            # vertical_alignment=ft.MainAxisAlignment.CENTER,
            # horizontal_alignment=ft.MainAxisAlignment.CENTER,
            route='/student/main',
            controls=[]
        )

    logout_button = ft.Container()
    logout_button.width = 200
    logout_button.height = 80
    logout_button.bgcolor = ft.colors.with_opacity(0.5, "white")
    logout_button.content = ft.Text("выйти", size=14, color='black')
    logout_button.border_radius = 8
    logout_button.alignment = ft.alignment.center
    logout_button.ink = True
    logout_button.on_hover = lambda e: on_hover(e)
    logout_button.scale = 1
    logout_button.animate_scale = ft.animation.Animation(800, ft.AnimationCurve.EASE_OUT)

    logout_button.gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.top_right,
        colors=["#D64511", "#B63621"]
    )
    logout_button.on_click = lambda _: page.go('/')  # handler
    #
    # Logo
    #
    logo_image = ft.Image(src=LOGO_PATH, width=200, height=200)
    # logo_image.top = 0
    # logo_image.left = 500
    logo_image.expand = True

    controls = [
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[logo_image]),
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
               controls=[containers.home_container, containers.courses_container]),
        ft.Container(height=40, expand=True),
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
               controls=[containers.grades_container, containers.tasks_container]),
        ft.Container(height=40, expand=True),
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[containers.profile_container]),  # bottom container
        # left log out button
        ft.Row(alignment=ft.MainAxisAlignment.END, controls=[logout_button, ft.Container(width=20)], expand=True)
    ]

    return ft.View(
        route='/student/main',
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[logo_image]),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                   controls=[containers.home_container, containers.courses_container]),
            ft.Container(height=40, expand=True),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                   controls=[containers.grades_container, containers.tasks_container]),
            ft.Container(height=40, expand=True),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[containers.profile_container]),
            # bottom container
            # left log out button
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[logout_button, ft.Container(width=20)],
                   expand=True)
        ]
    )
