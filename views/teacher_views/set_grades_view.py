import flet as ft
from flet_route import Basket, Params

from database.database import TeacherDatabase
from utils.exceptions import DontHaveGrades, UserDontHaveGrade
from utils.routes_url import TeacherRoutes

db = TeacherDatabase()


def SetGradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    if len(page.views) > 2:
        page.views.pop()

    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    # region: Search
    def search(e: ft.ControlEvent) -> None:
        ...

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

    # endregion

    dont_have_students = ft.Text(
        'Пока нет студентов по этому курсу', size=25, color=ft.colors.INVERSE_SURFACE,
        visible=False, weight=ft.FontWeight.BOLD, opacity=0.5
    )

    # region: Tab
    def tabs_changed(e: ft.ControlEvent) -> None:
        """Фильтруем все оценки"""
        dont_have_students.visible = False
        status = ''
        if subjects_filter_tab.visible is True:
            status = subjects_filter_tab.tabs[subjects_filter_tab.selected_index].text
        if student_filter_tab.visible is True:
            status = student_filter_tab.tabs[student_filter_tab.selected_index].text
        subjects.controls.clear()
        if status == 'Все' or status == 'Мои студенты' or status == 'Предметы' or status == 'Студенты':
            return
        else:
            subjects.controls.clear()
            students.controls.clear()
            try:
                # for _grade in sub_db.database.get_student_task_grades_with_subject_name(
                #         USER_ID, status
                # ):
                #     create_task_grade_card(
                #         subject_title=f'Предмет: {_grade.subject_task.subject.subject_name}',
                #         grade_value=f"{_grade.grade_value}",
                #         grade_date=f'Дата оценки: {_grade.grade_date.strftime("%d-%m-%Y")}',
                #         name_of_task=_grade.subject_task.task_name,
                #         grades=tasks_grades
                #     )
                ...
            except UserDontHaveGrade:
                dont_have_students.visible = True
                e.page.update()
        e.page.update()

    def filter_change(e: ft.ControlEvent) -> None:
        """Фильтруем фильтры которые у нас есть"""
        filter_name = filter_for_filter.tabs[filter_for_filter.selected_index].text
        if filter_name == 'Все':
            student_filter_tab.visible = False
            subjects_filter_tab.visible = False

        elif filter_name == 'Мои студенты':
            student_filter_tab.visible = True
            subjects_filter_tab.visible = False

        elif filter_name == 'Предметы':
            student_filter_tab.visible = False
            subjects_filter_tab.visible = True

        elif filter_name == 'Студенты':
            student_filter_tab.visible = True
            subjects_filter_tab.visible = False
        e.page.update()

    filter_for_filter = ft.Tabs(
        tabs=[ft.Tab(text='Все'), ft.Tab(text='Мои студенты'), ft.Tab(text='Предметы'), ft.Tab(text='Студенты')],
        on_change=filter_change,
    )
    students_tabs = []
    try:
        students = db.get_teacher_students(USER_ID)
        for student in students:
            name = f'{student[2]} {student[1]}'
            students_tabs.append(ft.Tab(text=f'{name}'))
    except DontHaveGrades as ex:
        dont_have_students.visible = True
        page.update()

    subjects_tabs = []
    try:
        subjects = db.get_teacher_subjects(USER_ID)
        for subject in subjects:
            subjects_tabs.append(ft.Tab(text=f'{subject.subject_name}'))
    except DontHaveGrades as ex:
        dont_have_students.visible = True
        page.update()

    student_filter_tab = ft.Tabs(
        scrollable=True,
        on_change=tabs_changed,
        tabs=students_tabs,
        visible=False
    )

    subjects_filter_tab = ft.Tabs(
        scrollable=True,
        on_change=tabs_changed,
        tabs=subjects_tabs,
        visible=False
    )

    # endregion

    # all content will be here
    students = ft.ResponsiveRow()

    subjects = ft.ResponsiveRow()

    content = ft.Column(
        [
            ft.Row([search_field, search_button]),
            ft.Column([
                ft.Row([filter_for_filter, student_filter_tab, subjects_filter_tab]),
                students,
                dont_have_students
            ], spacing=25)
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
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.GRADES_URL,
        controls=[
            main_container
        ]
    )
