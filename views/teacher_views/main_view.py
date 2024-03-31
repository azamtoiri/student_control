import flet as ft
from flet_route import Params, Basket

from constants import LOGO_PATH
from user_controls.modal_alert_dialog import ModalAlertDialog
from user_controls.student_container import STContainer
from utils.routes_url import TeacherRoutes, BaseRoutes


class TeacherContainers:
    def __init__(self):
        # TODO: Refactor code
        # home container
        self.home_container = STContainer(
            ft.Text('Домашняя страница', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6)
        # courses container
        self.courses_container = STContainer(
            content=ft.Text('Мои курсы', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6)
        self.grades_container = STContainer(
            content=ft.Text('Оценить студента', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
            alignment=ft.alignment.center, col=6
        )
        self.tasks_container = STContainer(
            content=ft.Text('Задания к курсам ', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
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


def TeacherMainView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    #
    # Button
    #
    containers = TeacherContainers()
    exit_dlg = ModalAlertDialog(
        title=ft.Text('Подтвердите действие'),
        content=ft.Text('Вы точно хотите выйти?'),
        yes_click=lambda e: exit_click(e),
    )

    # region: Functions
    def home_click(e: ft.ControlEvent) -> None:
        page.go(TeacherRoutes.HOME_URL)

    def courses_click(e: ft.ControlEvent) -> None:
        page.go(TeacherRoutes.SUBJECTS_URL)

    def grades_click(e: ft.ControlEvent) -> None:
        page.go(TeacherRoutes.GRADES_URL)

    def profile_click(e: ft.ControlEvent) -> None:
        page.go(BaseRoutes.TODO_URL)

    def tasks_click(e: ft.ControlEvent) -> None:
        page.go(TeacherRoutes.TASKS_URL)

    def exit_click(e: ft.ControlEvent) -> None:
        page.session.clear()
        page.go(BaseRoutes.INDEX_URL)

    def open_dlg_click(e: ft.ControlEvent):
        page.dialog = exit_dlg
        exit_dlg.dlg.open = True
        page.update()
        exit_dlg.dlg.update()

    # endregion

    # region: handlers
    containers.home_container.main_container.on_click = lambda e: home_click(e)
    containers.grades_container.main_container.on_click = lambda e: grades_click(e)
    containers.tasks_container.main_container.on_click = lambda e: tasks_click(e)
    containers.to_do.main_container.on_click = lambda e: profile_click(e)
    containers.courses_container.main_container.on_click = lambda e: courses_click(e)
    containers.exit_container.main_container.on_click = lambda e: open_dlg_click(e)

    # endregion

    logo_image = ft.Image(src=LOGO_PATH, width=200, height=200)
    # logo_image.top = 0
    # logo_image.left = 500
    # logo_image.expand = True

    teacher_title = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text('Fox', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.Text('Hub', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_ACCENT),
            ft.Text('Преподаватель', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREY)
        ]
    )

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.MAIN_URL,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[logo_image, teacher_title]),
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
