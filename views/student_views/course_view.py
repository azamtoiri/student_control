import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase

st_db = StudentDatabase()


def CourseView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    course = st_db.get_course_by_id(params.get('id'))

    # region: Functions
    def submit_click(e: ft.ControlEvent) -> None:
        ...

    # endregion

    # region: Buttons
    submit_button = ft.ElevatedButton('Записаться на курс')
    submit_button.on_click = lambda e: submit_click(e)

    # endregion

    # region: Text fields
    course_name = ft.Text(course.subject_name)
    course_description = ft.Text(course.description)

    # endregion

    content = ft.Column()
    content.controls.append(ft.Row([course_name]))
    content.controls.append(ft.Row([course_description]))
    content.controls.append(ft.Row([submit_button]))

    return ft.View(
        route='/course/:id',
        controls=[
            ft.Text(f'course id: {params.get("id")}'),
            content,
        ]
    )
