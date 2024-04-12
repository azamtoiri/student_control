import flet as ft
from flet_route import Basket, Params

from database.database import StudentDatabase
from user_controls.modal_alert_dialog import ModalAlertDialog
from user_controls.teacher_cards import create_student_task_card
from utils.banners import display_success_banner
from utils.routes_url import TeacherRoutes


async def SetGradeDetailView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    """Get subject ID and show all grades of student of this subject"""
    SUBJECT_ID = params.get('subject_id')
    STUDENT_ID = params.get('student_id')
    USER_ID = page.session.get('user_id')
    USER_NAME = page.session.get('username')

    db = StudentDatabase()
    HAVE_FINAL_GRADE = db.have_final_grade_for_subject(STUDENT_ID, SUBJECT_ID)

    set_final_grade_dlg = ModalAlertDialog(
        title=ft.Text('Поставить итоговую оценку'),
        content=ft.Column(
            controls=[
                ft.TextField(hint_text='Итоговая оценка'),
            ], height=80, adaptive=True
        ),
        yes_click=lambda e: yes_click(e)
    )

    def show_dlg(e: ft.ControlEvent) -> None:
        e.page.dialog = set_final_grade_dlg
        set_final_grade_dlg.dlg.open = True
        e.page.update()
        set_final_grade_dlg.update()

    def yes_click(e: ft.ControlEvent) -> None:
        _grade_value = int(set_final_grade_dlg.dlg.content.controls[0].value)
        if _grade_value > 100 or _grade_value < 0:
            set_final_grade_dlg.dlg.content.controls[0].error_text = 'Оценка должна быть не больше 100 и больше 0'
            set_final_grade_dlg.update()
            return
        db.set_final_grade_for_subject(STUDENT_ID, SUBJECT_ID, _grade_value)
        set_final_grade_dlg.dlg.open = False
        set_final_grade_dlg.update()
        final_grade_value.value = f'Итоговая оценка: {_grade_value}'
        final_grade_value.visible = True
        display_success_banner(page=page, message='Итоговая оценка поставлена', icons=ft.icons.GRADE)
        e.page.update()

    # region: save_file
    save_file_dialog = ft.FilePicker()
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
            db=db,
            task_file_url=i[0].task_files.task_file if i[0].task_files else None
        )

    # endregion

    # region: final grade
    _value = db.get_final_grade_for_subject(STUDENT_ID, SUBJECT_ID)
    final_grade_value = ft.Text(
        f'Итоговая оценка: {_value if _value else None}', size=25, color=ft.colors.INVERSE_SURFACE,
        weight=ft.FontWeight.BOLD, opacity=0.5, text_align=ft.TextAlign.CENTER, visible=True if _value else False
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
        visible=False
    )

    # endregion

    # region: search
    def search(e: ft.ControlEvent) -> None:
        search_value = str(search_field.value).strip()

    search_field = ft.TextField(
        hint_text='Найти предмет',
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
        on_click=lambda e: show_dlg(e),
        visible=False if HAVE_FINAL_GRADE else True
    )
    # endregion

    content = ft.Column(
        [
            ft.Row([search_field, search_button, set_final_grade_icon_button]),
            filter_tab,
            final_grade_value,
            student_grades_subject
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    # Background container for color and other
    main_container = ft.Container(
        border_radius=8,
        padding=ft.padding.all(10), bgcolor=ft.colors.SURFACE_VARIANT,
        content=content,
    )

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route=TeacherRoutes.SET_GRADE_DETAIL_URL,
        bgcolor=ft.colors.SURFACE_VARIANT,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            # content
            main_container
        ]
    )
