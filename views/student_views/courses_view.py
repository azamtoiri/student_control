import flet as ft
from flet_route import Params, Basket

from user_controls.tasks_card import TasksCard


def CoursesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # delete the last view duplicated view
    if len(page.views) > 1:
        page.views.pop()

    # region: Functions
    def tabs_changed(e):
        pass

    def add_text(e):
        tasks.controls.append()
        tasks.update()

    def add_course(_course_name: str, _course_description: str, course_url: str) -> None:
        course_title = ft.Text()
        course_title.value = _course_name

        course_description = ft.Text()
        course_description.value = _course_description

        show_course = ft.ElevatedButton('Посмотреть курс')
        show_course.on_click = lambda e: page.go(course_url)

        _card = ft.Card(col={"md": 12, "lg": 4})
        _card.content = ft.Container(content=ft.Column([
            ft.ListTile(leading=ft.Icon(ft.icons.TASK), title=course_title, subtitle=course_description),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[show_course])
        ]), width=400, padding=10)
        tasks.controls.append(_card)

    # endregion

    search = ft.TextField(
        hint_text="What needs to be done?", expand=True, filled=True
    )

    tasks = ft.ResponsiveRow()

    filter = ft.Tabs(
        scrollable=False,
        selected_index=0,
        on_change=tabs_changed,
        tabs=[ft.Tab(text='Все'), ft.Tab(text='Записанные'), ft.Tab(text='Завершенные')],
        # label_color=
    )

    content = ft.Column(
        [
            ft.Row([search, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=lambda e: add_text(e))]),
            ft.Column([
                filter,
                tasks
            ], spacing=25)
        ], scroll=ft.ScrollMode.ADAPTIVE
    )

    # Background container for color and other
    main_container = ft.Container(bgcolor=ft.colors.AMBER_300, border_radius=8, padding=ft.padding.all(10))
    main_container.content = content
    main_container.expand = True

    for i in range(1, 11):
        add_course(f'test {i}', f'test {i}', f'/course/{i}')
        # tasks.controls.append(
        #     TasksCard(f'Test {i}', f'More info {i}', f'/test/{i}')
        # )

    return ft.View(
        route='/student/courses',
        controls=[
            main_container
        ]
    )
