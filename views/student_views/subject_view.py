import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from user_controls.subject_description import SubjectDescription
from utils.banners import display_success_banner
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes

sub_db = LazyDatabase(StudentDatabase)

dlg = ft.AlertDialog(adaptive=True)


async def SubjectView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # course models
    course = sub_db.database.get_course_by_id(params.get('id'))

    # CONSTANTS
    USERNAME = page.session.get('username')
    USER_ID = page.session.get('user_id')
    SUBJECT_ID = params.get('id')

    # region: Functions
    def close_dlg(e: ft.ControlEvent) -> None:
        dlg.open = False
        e.page.update()

    def yes_click(e: ft.ControlEvent) -> None:
        sub_db.database.subscribe_student_to_subject(USER_ID, SUBJECT_ID)
        subscribe_button.visible = False
        unsubscribe_button.visible = True
        display_success_banner(page=e.page, message='Вы успешно зарегистрировались на курс',
                               icons=ft.icons.CHECK_CIRCLE)
        e.page.update()
        close_dlg(e)

    def yes_un_click(e: ft.ControlEvent) -> None:
        sub_db.database.unsubscribe_student_from_subject(USER_ID, SUBJECT_ID)
        subscribe_button.visible = True
        unsubscribe_button.visible = False
        display_success_banner(page=e.page, message='Вы успешно отписались от курса',
                               icons=ft.icons.MARK_AS_UNREAD)
        e.page.update()
        close_dlg(e)

    def no_click(e: ft.ControlEvent) -> None:
        close_dlg(e)

    def subscribe_dialog(e: ft.ControlEvent):
        dlg.actions = [
            ft.ElevatedButton('Да', on_click=yes_click, bgcolor=ft.colors.SURFACE_TINT,
                              color=ft.colors.WHITE, height=40
                              ),
            ft.ElevatedButton('Нет', on_click=no_click, bgcolor=ft.colors.GREY, color=ft.colors.WHITE)
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.CENTER
        dlg.modal = True
        dlg.icon = ft.Icon(ft.icons.WARNING, color=ft.colors.DEEP_ORANGE)
        dlg.title = ft.Text('Подтвердите действие')
        dlg.content = ft.Text('Вы точно хотите записаться на курс?')
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    def unsubscribe_dialog(e: ft.ControlEvent):
        dlg.actions = [
            ft.ElevatedButton('Да', on_click=yes_un_click, bgcolor=ft.colors.SURFACE_TINT,
                              color=ft.colors.WHITE),
            ft.ElevatedButton('Нет', on_click=no_click, bgcolor=ft.colors.GREY, color=ft.colors.WHITE,
                              height=40)
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.CENTER
        dlg.modal = True
        dlg.icon = ft.Icon(ft.icons.WARNING, color=ft.colors.DEEP_ORANGE)
        dlg.title = ft.Text('Подтвердите действие')
        dlg.content = ft.Text('Вы точно хотите записаться на курс?')
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    def subscribe_click(e: ft.ControlEvent) -> None:
        subscribe_dialog(e)
        e.page.update()

    def unsubscribe_click(e: ft.ControlEvent) -> None:
        unsubscribe_dialog(e)
        e.page.update()

    # endregion
    is_subscribed = sub_db.database.check_student_subscribe(USER_ID, SUBJECT_ID)

    # region: Buttons
    subscribe_button = ft.ElevatedButton('Записаться на курс')
    subscribe_button.on_click = lambda e: subscribe_click(e)
    subscribe_button.color = ft.colors.WHITE
    subscribe_button.bgcolor = ft.colors.SURFACE_TINT
    subscribe_button.visible = not is_subscribed

    unsubscribe_button = ft.ElevatedButton('Отписаться от курса')
    unsubscribe_button.on_click = lambda e: unsubscribe_click(e)
    unsubscribe_button.color = ft.colors.WHITE
    unsubscribe_button.bgcolor = ft.colors.INVERSE_SURFACE
    unsubscribe_button.visible = is_subscribed

    # endregion

    # region: Text fields
    course_name = ft.Text(course.subject_name)
    course_description = ft.Text(course.description)

    # endregion

    content = ft.Column(
        controls=[
            SubjectDescription(SUBJECT_ID),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[subscribe_button]),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[unsubscribe_button])
        ]
    )

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.SUBJECT_URL,
        controls=[
            content,
        ]
    )
