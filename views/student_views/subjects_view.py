import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from utils.exceptions import DontHaveGrades

st_db = StudentDatabase()


def SubjectsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # delete the last view duplicated view
    if len(page.views) > 1:
        page.views.pop()

    def add_all_subjects():
        all_subjects = st_db.get_all_subjects()

        for subject in all_subjects:
            is_subscribed = st_db.check_student_subscribe(page.session.get('user_id'), subject.subject_id)
            print(is_subscribed)
            subject_add(
                f'Имя курса: {subject.subject_name}',
                f'Описание: {subject.description}',
                f'/course/{subject.subject_id}',
                is_subscribed
            )

    # region: Functions
    def tabs_changed(e: ft.ControlEvent) -> None:
        # get user that he is subscribed to subject
        status = filter.tabs[filter.selected_index].text
        subjects.controls.clear()
        # set visible false to text
        if dont_have_subjects:
            dont_have_subjects.visible = False
        try:
            if status == 'Записанные':
                values = st_db.get_student_subjects(e.page.session.get('username'), e.page.session.get('user_id'))
                for first_name, enrollment, subject_name, subject_description, subject_id in values:
                    is_subscribed = st_db.check_student_subscribe(page.session.get('user_id'), subject_id)
                    print(is_subscribed)
                    subject_add(
                        f"Имя курса: {subject_name}",
                        f"Описание: {subject_description}",
                        f'/course/{subject_id}',
                        is_subscribed
                    )
                    e.page.update()
            else:
                add_all_subjects()
            e.page.update()
        except DontHaveGrades:
            subjects.controls.clear()
            # set visible True to this text
            dont_have_subjects.visible = True
            e.page.update()

    def search(e):
        ...
        # tasks.controls.append()
        # tasks.update()

    def subject_add(subject_name: str, subject_description: str, subject_url: str, is_subscribed=False) -> None:
        course_title = ft.Text()
        course_title.value = subject_name

        course_description = ft.Text()
        course_description.value = subject_description

        show_course = ft.ElevatedButton('Посмотреть курс')
        show_course.bgcolor = ft.colors.ORANGE_ACCENT
        show_course.color = ft.colors.WHITE
        show_course.on_click = lambda e: page.go(subject_url)

        subject_icon = ft.Icon(ft.icons.TASK)
        subject_icon.color = ft.colors.GREEN if is_subscribed else ft.colors.GREY

        _card = ft.Card(col={"md": 12, "lg": 4})
        _card.color = ft.colors.ORANGE_50
        _card.content = ft.Container(content=ft.Column([
            ft.ListTile(leading=subject_icon, title=course_title, subtitle=course_description),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[show_course])
        ]), width=400, padding=10)
        subjects.controls.append(_card)

    # endregion

    search = ft.TextField(
        hint_text="Введите имя курса", expand=True, filled=True, bgcolor='white', border_radius=8
    )
    search.on_submit = lambda e: search(e)

    subjects = ft.ResponsiveRow()
    dont_have_subjects = ft.Text('У вас нет записанных курсов', size=20, color=ft.colors.WHITE)
    dont_have_subjects.visible = False

    filter = ft.Tabs(
        scrollable=False,
        selected_index=0,
        on_change=tabs_changed,
        tabs=[ft.Tab(text='Все'), ft.Tab(text='Записанные')],
        animation_duration=100,
    )

    content = ft.Column(
        [
            ft.Row([search, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=lambda e: search(e),
                                                    bgcolor=ft.colors.ORANGE_ACCENT_200)]),
            ft.Column([
                filter,
                subjects,
                dont_have_subjects
            ], spacing=25)
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    # Background container for color and other
    main_container = ft.Container(bgcolor=ft.colors.ORANGE_ACCENT_100, border_radius=8, padding=ft.padding.all(10))
    main_container.content = content
    main_container.expand = True

    # add all subjects
    add_all_subjects()
    return ft.View(
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        route='/student/courses',
        controls=[
            main_container
        ]
    )
