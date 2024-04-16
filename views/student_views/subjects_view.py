import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from utils.exceptions import DontHaveGrades
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes

st_db = LazyDatabase(StudentDatabase)


async def SubjectsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # delete the last view duplicated view
    if len(page.views) > 1:
        page.views.pop()

    async def add_all_subjects():
        try:
            all_subjects = st_db.database.get_all_subjects()

            for subject in all_subjects:
                is_subscribed = st_db.database.check_student_subscribe(
                    page.session.get('user_id'),
                    subject.subject_id
                )
                await subject_add(
                    f'{subject.subject_name}',
                    f'{subject.short_description}',
                    f'{StudentRoutes.SIMPLE_SUBJECT_URL}/{subject.subject_id}',
                    is_subscribed,
                    subject.users.first_name,
                    subject.users.middle_name,
                )
        except Exception as err:
            print(err)

    # region: Functions
    async def tabs_changed(e: ft.ControlEvent) -> None:
        # get user that he is subscribed to subject
        status = _filter.tabs[_filter.selected_index].text
        subjects.controls.clear()
        # set visible false to text
        if dont_have_subjects:
            dont_have_subjects.visible = False
        try:
            if status == 'Записанные':
                values = st_db.database.get_student_subjects(
                    e.page.session.get('username'),
                    e.page.session.get('user_id')
                )
                for first_name, enrollment, subject_name, subject_description, subject in values:
                    is_subscribed = st_db.database.check_student_subscribe(
                        page.session.get('user_id'),
                        subject.subject_id
                    )
                    await subject_add(
                        f"{subject_name}",
                        f"{subject_description}",
                        f'/subject/{subject.subject_id}',
                        is_subscribed,
                        subject.users.first_name,
                        subject.users.middle_name,

                    )
                    e.page.update()
            else:
                await add_all_subjects()
            e.page.update()
        except DontHaveGrades:
            subjects.controls.clear()
            # set visible True to this text
            dont_have_subjects.visible = True
            e.page.update()

    async def search(e: ft.ControlEvent):
        subjects.controls.clear()
        search_value = str(search_field.value).strip() if len(search_field.value) else None
        if search_value is None:
            await add_all_subjects()
            e.page.update()
            return
        filtered_subjects = st_db.database.filter_subjects_by_name(str(search_field.value).strip())
        for subject in filtered_subjects:
            is_subscribed = st_db.database.check_student_subscribe(page.session.get('user_id'),
                                                                   subject.subject_id)
            await subject_add(
                f"{subject.subject_name}",
                f'Описание: {subject.short_description}',
                f'/course/{subject.subject_id}',
                is_subscribed,
                subject.users.first_name,
                subject.users.middle_name,

            )
        e.page.update()

    async def subject_add(
            subject_name: str, subject_description: str, subject_url: str, is_subscribed=False,
            teacher_name: str = None, teacher_last_name: str = None
    ) -> None:
        """Subject card control"""
        course_title = ft.Text()
        course_title.value = subject_name

        course_description = ft.Text()
        course_description.value = subject_description

        show_course = ft.ElevatedButton('Посмотреть курс')
        show_course.bgcolor = ft.colors.ON_SURFACE_VARIANT
        show_course.color = ft.colors.WHITE
        show_course.on_click = lambda e: page.go(subject_url)

        subject_icon = ft.Icon(ft.icons.TASK)
        subject_icon.color = ft.colors.SURFACE_TINT if is_subscribed else ft.colors.GREY

        _card = ft.Card(col={"md": 12, "lg": 4})
        _card.color = ft.colors.SURFACE_VARIANT
        _card.content = ft.Container(content=ft.Column([
            ft.ListTile(leading=subject_icon, title=course_title, subtitle=course_description),
            ft.Row(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON),
                        title=ft.Row([ft.Text(teacher_name), ft.Text(teacher_last_name)]),
                    ),
                ]
            ),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[show_course])
        ]), width=400, padding=10)
        subjects.controls.append(_card)

    def on_focus_search_field(e: ft.ControlEvent) -> None:
        search_field.hint_text = None
        e.page.update()

    def un_focus_search_field(e: ft.ControlEvent) -> None:
        search_field.hint_text = "Введите имя курса"
        e.page.update()

    # endregion

    search_field = ft.TextField(
        hint_text="Введите имя курса", expand=True, filled=True, bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=8,
        adaptive=True
    )
    search_field.on_submit = search
    search_field.on_focus = lambda e: on_focus_search_field(e)
    search_field.on_blur = lambda e: un_focus_search_field(e)

    subjects = ft.ResponsiveRow()

    dont_have_subjects = ft.Text(
        'У вас нет записанных курсов', size=25, color=ft.colors.INVERSE_SURFACE,
        visible=False, weight=ft.FontWeight.BOLD, opacity=0.5
    )

    _filter = ft.Tabs(
        scrollable=True,
        selected_index=0,
        on_change=tabs_changed,
        tabs=[ft.Tab(text='Все'), ft.Tab(text='Записанные')],
        animation_duration=100,
    )

    content = ft.Column(
        [
            ft.Row([search_field, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=lambda e: search(e),
                                                          bgcolor=ft.colors.SURFACE_VARIANT)]),
            ft.Column([
                _filter,
                subjects,
                dont_have_subjects
            ], spacing=25)
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    # Background container for color and other
    main_container = ft.Container(
        border_radius=8,
        padding=ft.padding.all(10), bgcolor=ft.colors.SURFACE_VARIANT
    )
    main_container.content = content
    main_container.expand = True

    # add all subjects
    await add_all_subjects()
    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route=StudentRoutes.SUBJECTS_URL,
        controls=[
            main_container
        ]
    )
