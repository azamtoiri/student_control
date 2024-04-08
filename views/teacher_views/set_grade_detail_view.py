import flet as ft
from flet_route import Basket, Params

from database.database import StudentDatabase
from user_controls.modal_alert_dialog import ModalAlertDialog
from user_controls.teacher_cards import create_student_task_card
from utils.routes_url import TeacherRoutes


def SetGradeDetailView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    """Get subject ID and show all grades of student of this subject"""
    SUBJECT_ID = params.get('subject_id')
    STUDENT_ID = params.get('student_id')
    USER_ID = page.session.get('user_id')
    USER_NAME = page.session.get('username')

    db = StudentDatabase()

    set_grade_dlg = ModalAlertDialog(
        title=ft.Text('Поставить оценку'),
        content=ft.Column(
            controls=[
                ft.TextField(hint_text='Оценка'),
            ], height=80, adaptive=True
        ),
        yes_click=lambda _: print("Yes")
    )

    # region: save_file
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            raise NotImplemented()

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    student_grades_subject = ft.ResponsiveRow()

    for i in db.get_student_subject_tasks_by_subject_id(STUDENT_ID, SUBJECT_ID):
        create_student_task_card(
            task_title=f'{i[0].task_name}',
            task_upload_date=f'{" " if i[4] is None else i[4].grade_date.strftime("%d.%m.%Y") if i[4].grade_date else None}',
            student_fio=f'{i[1].last_name} {i[1].first_name}',
            grade_value=f'{"Нет оценки" if i[4] is None else i[4].grade_value if i[4].grade_value else "Нет оценки"}',
            grades=student_grades_subject,
            save_file_dialog=save_file_dialog,
            enrollment_id=i[3].enrollment_id,
            subject_task_id=i[0].subject_task_id,
            user_id=i[1].user_id,
            db=db
        )

    # endregion

    # region: Filter Tab
    def tab_changed(e: ft.ControlEvent):
        ...

    tabs = [ft.Tab('Все')]
    filter_tab = ft.Tabs(
        scrollable=True,
        on_change=tab_changed,
        tabs=tabs,
    )

    # endregion

    # region: search
    def search(e: ft.ControlEvent) -> None:
        raise NotImplemented('')

    search_field = ft.TextField(
        hint_text="Найти студента",
        on_submit=lambda e: search(e),
        border_radius=8,
        expand=True,
        tooltip='Имя студента'
    )

    search_button = ft.FloatingActionButton(
        icon=ft.icons.SEARCH,
        bgcolor=ft.colors.SURFACE_TINT,
        on_click=lambda e: search(e),
        tooltip='Поиск'
    )

    set_final_grade_icon_button = ft.IconButton(
        icon=ft.icons.GRADE,
        tooltip='Поставить итоговую оценку',
    )
    # endregion

    content = ft.Column(
        [
            ft.Row([search_field, search_button, set_final_grade_icon_button]),
            filter_tab,
            student_grades_subject
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    # Background container for color and other
    main_container = ft.Container(
        border_radius=8,
        padding=ft.padding.all(10), bgcolor=ft.colors.SURFACE_VARIANT,
        content=content,
        # expand=True
    )

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route=TeacherRoutes.SET_GRADE_DETAIL_URL,
        bgcolor=ft.colors.SURFACE_VARIANT,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            main_container
        ]
    )
