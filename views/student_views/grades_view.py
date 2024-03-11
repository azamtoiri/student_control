import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from utils.exceptions import DontHaveGrades, UserDontHaveGrade

sub_db = StudentDatabase()


def GradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    def add_grades():
        """adding user grades"""
        for grade in sub_db.get_student_grades(page.session.get('username')):
            add_grade(f'Предмет: {grade[1]}', f"{grade[2]}", f"Дата оценки: {grade[3].strftime('%d-%m-%Y')}")

    def add_grade(subject_title: str, grade_value: str, grade_date: str) -> None:
        """Add grade card"""
        _grade_value = ft.Text(f'Оценка {grade_value}')

        _subject_title = ft.Text(subject_title)

        _grade_date = ft.Text(grade_date)

        _card = ft.Card(col={"md": 12, "lg": 4})
        if int(grade_value) == 100:
            _card.color = ft.colors.GREEN
        elif int(grade_value) >= 80:
            _card.color = ft.colors.GREEN_ACCENT_100
        else:
            _card.color = ft.colors.RED
        _card.content = ft.Container(content=ft.Column([
            ft.ListTile(leading=ft.Icon(ft.icons.GRADE_OUTLINED), title=_grade_value,
                        subtitle=ft.Column([_subject_title, _grade_date], adaptive=True)),
            ft.Row(alignment=ft.MainAxisAlignment.END)
        ]), width=400, padding=10)
        grades.controls.append(_card)

    def tabs_changed(e: ft.ControlEvent) -> None:
        """Function for filtering in filter tab"""
        no_grades.visible = False
        status = filter_tab.tabs[filter_tab.selected_index].text
        grades.controls.clear()
        if status == 'Все':
            add_grades()
        else:
            try:
                for _grade in sub_db.get_student_grade_for_exact_subject(e.page.session.get('username'), status):
                    add_grade(f'Предмет: {_grade[1]}', f"{_grade[2]}",
                               f"Дата оценки: {_grade[3].strftime('%d-%m-%Y')}")
            except UserDontHaveGrade:
                no_grades.value = 'Нет оценок по этому предмету'
                no_grades.visible = True
                e.page.update()
        e.page.update()

    # the row that contains all grade controls on this page
    grades = ft.ResponsiveRow()

    # hided text if you don't have grades
    no_grades = ft.Text('У вас нет оценок', size=25, color=ft.colors.GREY)
    no_grades.visible = False

    # list for tabs [default contains 'Все']
    tabs = [ft.Tab('Все')]
    # get all subjects and add to tabs
    try:
        subjects = sub_db.get_student_subjects(page.session.get('username'))

        for subject in subjects:
            tabs.append(ft.Tab(str(subject.subject_name)))
    except DontHaveGrades as ex:
        no_grades.value = 'У вас нет оценок'
        no_grades.visible = True
        page.update()

    # tab for filtering grades
    filter_tab = ft.Tabs(
        scrollable=True,
        selected_index=0,
        on_change=tabs_changed,
        tabs=tabs
    )

    # adding user grades to the page
    add_grades()

    return ft.View(
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        route='/student/grades',
        controls=[
            filter_tab,
            grades,
            no_grades,
        ]
    )
