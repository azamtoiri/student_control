from typing import Any

import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase

sub_db = StudentDatabase()

dlg = ft.AlertDialog()


def SubjectView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # course models
    course = sub_db.get_course_by_id(params.get('id'))

    # CONSTANTS
    USERNAME = page.session.get('username')
    USER_ID = page.session.get('user_id')
    SUBJECT_ID = params.get('id')

    # region: Functions
    def close_dlg(e: ft.ControlEvent) -> None:
        dlg.open = False
        e.page.update()

    def yes_click(e: ft.ControlEvent) -> None:
        sub_db.subscribe_student_to_subject(USER_ID, SUBJECT_ID)
        close_dlg(e)

    def yes_un_click(e: ft.ControlEvent) -> None:
        sub_db.unsubscribe_student_from_subject(USER_ID, SUBJECT_ID)
        close_dlg(e)

    def no_click(e: ft.ControlEvent) -> None:
        close_dlg(e)

    def subscribe_dialog(e: ft.ControlEvent):
        dlg.actions = [
            ft.ElevatedButton('Да', on_click=lambda e_: yes_click(e_)),
            ft.ElevatedButton('Нет', on_click=lambda e_: no_click(e_))
        ]
        dlg.modal = True
        dlg.icon = ft.Icon(ft.icons.WARNING)
        dlg.title = ft.Text('Подтвердите действие')
        dlg.content = ft.Text('Вы точно хотите записаться на курс?')
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    def unsubscribe_dialog(e: ft.ControlEvent):
        dlg.actions = [
            ft.ElevatedButton('Да', on_click=lambda e_: yes_un_click(e_)),
            ft.ElevatedButton('Нет', on_click=lambda e_: no_click(e_))
        ]
        dlg.modal = True
        dlg.icon = ft.Icon(ft.icons.WARNING)
        dlg.title = ft.Text('Подтвердите действие')
        dlg.content = ft.Text('Вы точно хотите записаться на курс?')
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    def subscribe_click(e: ft.ControlEvent) -> None:
        subscribe_dialog(e)

    def unsubscribe_click(e: ft.ControlEvent) -> None:
        unsubscribe_dialog(e)

    # endregion
    is_subscribed = sub_db.check_student_subscribe(USER_ID, SUBJECT_ID)

    # region: Buttons
    subscribe_button = ft.ElevatedButton('Записаться на курс')
    subscribe_button.on_click = lambda e: subscribe_click(e)
    subscribe_button.visible = not is_subscribed

    unsubscribe_button = ft.ElevatedButton('Отписаться от курса')
    unsubscribe_button.on_click = lambda e: unsubscribe_click(e)
    unsubscribe_button.visible = is_subscribed

    # endregion

    # region: Text fields
    course_name = ft.Text(course.subject_name)
    course_description = ft.Text(course.description)

    # endregion

    content = ft.Column()
    content.controls.append(ft.Row([course_name]))
    content.controls.append(ft.Row([course_description]))
    content.controls.append(ft.Row([subscribe_button]))
    content.controls.append(ft.Row([unsubscribe_button]))

    return ft.View(
        route='/course/:id',
        controls=[
            ft.Text(f'course id: {params.get("id")}'),
            content,
        ]
    )
