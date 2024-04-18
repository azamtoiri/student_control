import flet as ft
from flet_route import Basket, Params

from database.database import TeacherDatabase
from user_controls.teacher_cards import create_students_subject_card
from utils.exceptions import DontHaveGrades
from utils.routes_url import TeacherRoutes

db = TeacherDatabase()


async def SetGradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    if len(page.views) > 2:
        page.views.pop()

    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    # region: Search
    async def search(e: ft.ControlEvent) -> None:
        dont_have_students.visible = False
        await subjects_row.clean_async()
        await students_row.clean_async()
        search_value = str(search_field.value).strip()
        try:
            list_subjects = await db.get_teacher_students_with_filter(USER_ID, search_value)
            print('list: sub', list_subjects)
            for list_subject in list_subjects:
                await create_students_subject_card(
                    subject_title=list_subject[3],
                    student_fio=f'{list_subject[2]} {list_subject[1]}',
                    student_row=students_row,
                    subject_url=f'/set-grade/{list_subject[4]}/{list_subject[0]}'
                )
            e.page.update()
        except DontHaveGrades:
            print(DontHaveGrades)
            dont_have_students.value = 'Ничего не найдено'
            dont_have_students.visible = True
            e.page.update()

    search_field = ft.TextField(
        hint_text="Найти студента",
        on_submit=search,
        border_radius=8,
        expand=True,
        tooltip='Имя студента'
    )

    search_button = ft.FloatingActionButton(
        icon=ft.icons.SEARCH,
        bgcolor=ft.colors.SURFACE_TINT,
        on_click=search,
        tooltip='Поиск'
    )

    # endregion

    dont_have_students = ft.Text(
        'Пока нет студентов по этому курсу', size=25, color=ft.colors.INVERSE_SURFACE,
        visible=False, weight=ft.FontWeight.BOLD, opacity=0.5, text_align=ft.TextAlign.CENTER
    )

    # region: Tab
    async def tabs_changed(e: ft.ControlEvent) -> None:
        """Фильтруем все оценки по предметам"""
        dont_have_students.visible = False
        student_filter_tab.visible = False
        e.page.update()
        await subjects_row.clean_async()
        await students_row.clean_async()
        status = subjects_filter_tab.tabs[subjects_filter_tab.selected_index].text
        try:
            list_subjects = await db.get_teacher_students_subjects_with_filter(USER_ID, status)
            for list_subject in list_subjects:
                await create_students_subject_card(
                    subject_title=list_subject[3],
                    student_fio=f'{list_subject[2]} {list_subject[1]}',
                    student_row=subjects_row,
                    subject_url=f'/set-grade/{list_subject[4]}/{list_subject[0]}'
                )
        except DontHaveGrades:
            print(DontHaveGrades)
            dont_have_students.visible = True
            e.page.update()
        e.page.update()

    async def student_tabs_changed(e: ft.ControlEvent) -> None:
        """Фильтруем все оценки по студентам"""
        dont_have_students.visible = False
        subjects_filter_tab.visible = False
        e.page.update()
        status = str(student_filter_tab.tabs[student_filter_tab.selected_index].text).split()
        await students_row.clean_async()
        await subjects_row.clean_async()
        try:
            list_subjects = await db.get_teacher_students_with_filter(USER_ID, status[0])
            for list_subject in list_subjects:
                await create_students_subject_card(
                    subject_title=list_subject[3],
                    student_fio=f'{list_subject[2]} {list_subject[1]}',
                    student_row=students_row,
                    subject_url=f'/set-grade/{list_subject[4]}/{list_subject[0]}'
                )
        except DontHaveGrades:
            print(DontHaveGrades)
            dont_have_students.visible = True
            e.page.update()
        e.page.update()

    async def filter_change(e: ft.ControlEvent) -> None:
        """Фильтруем фильтры которые у нас есть"""
        dont_have_students.visible = False
        filter_name = filter_for_filter.tabs[filter_for_filter.selected_index].text
        if filter_name == 'Все':
            student_filter_tab.visible = False
            subjects_filter_tab.visible = False
            await subjects_row.clean_async()
            await students_row.clean_async()
            await show_all_subjects_row()

        elif filter_name == 'Предметы':
            student_filter_tab.visible = False
            subjects_filter_tab.visible = True

        elif filter_name == 'Студенты':
            student_filter_tab.visible = True
            subjects_filter_tab.visible = False
        e.page.update()

    filter_for_filter = ft.Tabs(
        tabs=[ft.Tab(text='Все'), ft.Tab(text='Предметы'), ft.Tab(text='Студенты')],
        on_change=filter_change,
    )

    students_tabs = []
    try:
        students_db = await db.get_teacher_students(USER_ID)
        for _student in students_db:
            name = f'{_student[2]} {_student[1]}'
            students_tabs.append(ft.Tab(text=f'{name}'))
    except DontHaveGrades as ex:
        print(ex)
        dont_have_students.visible = True
        page.update()
    except Exception as err:
        print(err)

    subjects_tabs = []
    try:
        _subjects = await db.get_teacher_subjects(USER_ID)
        for subject in _subjects:
            subjects_tabs.append(ft.Tab(text=f'{subject.subject_name}'))
    except DontHaveGrades as ex:
        print(ex)
        dont_have_students.visible = True
        page.update()

    student_filter_tab = ft.Tabs(
        scrollable=True,
        on_change=student_tabs_changed,
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
    students_row = ft.ResponsiveRow()

    subjects_row = ft.ResponsiveRow()

    async def show_all_subjects_row():
        try:
            list_subjects = await db.get_teacher_students_with_subjects(USER_ID)
            for list_subject in list_subjects:
                await create_students_subject_card(
                    subject_title=list_subject[3],
                    student_fio=f'{list_subject[2]} {list_subject[1]}',
                    student_row=subjects_row,
                    subject_url=f'/set-grade/{list_subject[4]}/{list_subject[0]}'
                )
        except Exception as err:
            print(err)

    await show_all_subjects_row()

    content = ft.Column(
        [
            ft.Row([search_field, search_button]),
            ft.Column([
                ft.Row(
                    [
                        ft.Icon(ft.icons.QUESTION_MARK, tooltip='Фильтр', size=15),
                        filter_for_filter, student_filter_tab,
                        subjects_filter_tab
                    ]
                ),
                students_row,
                subjects_row,
                dont_have_students
            ], spacing=25, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
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
