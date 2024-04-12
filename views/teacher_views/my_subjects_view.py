import flet as ft
from flet_route import Basket, Params

from database.database import StudentDatabase
from utils.lazy_db import LazyDatabase
from utils.routes_url import TeacherRoutes

# st_db = StudentDatabase()
st_db = LazyDatabase(StudentDatabase)


async def MySubjectsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # delete the last view duplicated view
    USER_ID = page.session.get('user_id')

    if len(page.views) > 2:
        page.views.pop()

    def add_all_subjects():
        all_subjects = st_db.database.get_teacher_subjects(USER_ID)

        for subject in all_subjects:
            # is_subscribed = st_db.database.check_student_subscribe(page.session.get('user_id'), subject.subject_id)
            subject_add(
                f'{subject.subject_name}',
                f'{subject.short_description}',
                f'{TeacherRoutes.SIMPLE_SUBJECT_URL}{subject.subject_id}',
            )

    # region: Functions
    def go_to_add_subject_page(e: ft.ControlEvent) -> None:
        e.page.route = TeacherRoutes.SUBJECT_ADD_URL
        e.page.update()

    def search(e: ft.ControlEvent):
        subjects.controls.clear()
        search_value = str(search_field.value).strip() if len(search_field.value) else None
        if search_value is None:
            add_all_subjects()
            e.page.update()
            return
        filtered_subjects = st_db.database.filter_subjects_by_name(str(search_field.value).strip())
        for subject in filtered_subjects:
            subject_add(
                f"{subject.subject_name}",
                f'{subject.description}',
                f'{TeacherRoutes.SIMPLE_SUBJECT_URL}{subject.subject_id}',
                # is_subscribed=is_subscribed,
            )
        e.page.update()

    def subject_add(subject_name: str, subject_description: str, subject_url: str, is_subscribed=False) -> None:
        """Subject card control"""
        course_title = ft.Text()
        course_title.value = subject_name

        course_description = ft.Text()
        course_description.value = subject_description

        show_course = ft.ElevatedButton('Изменить курс')
        show_course.bgcolor = ft.colors.ON_SURFACE_VARIANT
        show_course.color = ft.colors.WHITE
        show_course.on_click = lambda e: page.go(subject_url)

        subject_icon = ft.Icon(ft.icons.TASK)
        subject_icon.color = ft.colors.SURFACE_TINT if is_subscribed else ft.colors.GREY

        _card = ft.Card(col={"md": 12, "lg": 4})
        _card.color = ft.colors.SURFACE_VARIANT
        _card.content = ft.Container(content=ft.Column([
            ft.ListTile(leading=subject_icon, title=course_title, subtitle=course_description),
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
        hint_text="Введите имя курса",
        expand=True, filled=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=8, tooltip='Поиск',
        adaptive=True,
    )
    search_field.on_submit = lambda e: search(e)
    search_field.on_focus = lambda e: on_focus_search_field(e)
    search_field.on_blur = lambda e: un_focus_search_field(e)

    subjects = ft.ResponsiveRow()
    dont_have_subjects = ft.Text(
        'У вас нет записанных курсов', size=25, color=ft.colors.INVERSE_SURFACE,
        visible=False, weight=ft.FontWeight.BOLD, opacity=0.5
    )  # Warning text

    content = ft.Column(
        [
            ft.Row(
                [
                    search_field,
                    ft.FloatingActionButton(
                        icon=ft.icons.SEARCH, on_click=lambda e: search(e),
                        bgcolor=ft.colors.SURFACE_VARIANT, tooltip='Поиск'
                    ),  # Search button
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=lambda e: go_to_add_subject_page(e),
                        bgcolor=ft.colors.SURFACE_VARIANT, tooltip='Добавить курс'
                    )  # Subject add button
                ]
            ),
            ft.Column([
                subjects,
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[dont_have_subjects])
            ], spacing=25)
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    add_all_subjects()

    # Background container for color and other
    main_container = ft.Container(
        border_radius=8,
        padding=ft.padding.all(10), bgcolor=ft.colors.SURFACE_VARIANT
    )
    main_container.content = content
    main_container.expand = True

    # add all subjects

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.SUBJECTS_URL,
        controls=[main_container]
    )
